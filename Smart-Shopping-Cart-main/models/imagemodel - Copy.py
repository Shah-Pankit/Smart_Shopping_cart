import numpy as np
import cv2
from keras.utils import img_to_array
from keras.applications import vgg16
from keras.models import Model
from keras.layers import GlobalAveragePooling2D, Dense
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

class ImageModel:
    def __init__(self) -> None:
        self.all_labels = ["apple", "custard apple", "green grapes", "NOTHING", "papaya", "strawberry"]
        self.feature_extractor = self.initialize_feature_extractor()

    def initialize_feature_extractor(self):
        img_rows, img_cols = 224, 224

        vgg = vgg16.VGG16(weights='imagenet',
                          include_top=False,
                          input_shape=(img_rows, img_cols, 3))

        for layer in vgg.layers:
            layer.trainable = False

        def lw(bottom_model, num_classes):
            top_model = bottom_model.output
            top_model = GlobalAveragePooling2D()(top_model)
            top_model = Dense(256, activation='relu')(top_model)
            top_model = Dense(128, activation='relu')(top_model)
            top_model = Dense(96, activation='relu')(top_model)
            top_model = Dense(64, activation='relu')(top_model)
            top_model = Dense(num_classes, activation='softmax')(top_model)
            return top_model

        num_classes = 6
        FC_Head = lw(vgg, num_classes)
        feature_extractor = Model(inputs=vgg.input, outputs=FC_Head)

        feature_extractor.load_weights(r"../saved_models/final_model_weights - Copy.h5")

        # Extract features from the last dense layer (before softmax)
        feature_extractor = Model(inputs=vgg.input, outputs=feature_extractor.layers[-2].output)

        return feature_extractor

    def convert_image_to_array(self, image_dir):
        try:
            image = cv2.imread(image_dir)
            if image is not None:
                print("Image loaded successfully.")
                image = cv2.resize(image, (224, 224))
                image_array = img_to_array(image)
                image_array = np.array(image_array, dtype=np.float32) / 255
                image_array = image_array.reshape(-1, 224, 224, 3)
                return image_array
            else:
                print("Image is None. Check the image path.")
                return np.array([])
        except Exception as e:
            print(f"Error : {e}")
            return None

    def train_svm_classifier(self, features, labels):
        svm_classifier = svm.SVC(kernel='linear', C=1.0)
        svm_classifier.fit(features, labels)
        return svm_classifier

    def evaluate_svm_classifier(self, svm_classifier, features, labels):
        predictions = svm_classifier.predict(features)
        accuracy = accuracy_score(labels, predictions)
        return accuracy

    def predict_on_image(self, inputImageDir):
        inputImage = self.convert_image_to_array(inputImageDir)
        print(f"Input Image Shape: {inputImage.shape if inputImage is not None else 'None'}")

        if inputImage is not None:
            # Extract features using the feature extractor
            features = self.feature_extractor.predict(inputImage)

            # Load your training data and labels
            # Assuming you have a function load_training_data_labels() to load your data
            # Modify the function according to your data loading format
            X_train, X_test, y_train, y_test = load_training_data_labels()

            # Train an SVM classifier on the extracted features
            svm_classifier = self.train_svm_classifier(X_train, y_train)

            # Evaluate the SVM classifier on the test set
            accuracy = self.evaluate_svm_classifier(svm_classifier, X_test, y_test)

            print(f'SVM Accuracy: {accuracy}')

            # Make predictions using the SVM classifier
            svm_prediction = svm_classifier.predict(features)
            return self.all_labels[int(svm_prediction)]
        else:
            return "Unable to predict due to empty input."

# Assuming you have a function to load your training data and labels
def load_training_data_labels():
    labels = ["apple", "custard apple", "green grapes", "NOTHING", "papaya", "strawberry"]
    return labels
