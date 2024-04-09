import os
from new_imagemodel import imageModel
from collections import Counter
most_prediction = []
def makePredictionsForFolder(folder_path):
    imgModel = imageModel()
    predictions = []

    for image_file in os.listdir(folder_path)[::10]:
        if image_file.endswith(".jpg"):
            image_path = os.path.join(folder_path, image_file)
            predictions.append(imgModel.predict_on_image(image_path))

    # Find the most common prediction
    most_common_prediction = Counter(predictions).most_common(1)
    
    if most_common_prediction:
        most_prediction.append(most_common_prediction[0][0])
        return most_prediction
    else:
        return "No predictions."

# Example usage:
# jpg_folder = r"../prediction/new_prediction_frames/NOTHING/"
# result = makePredictionsForFolder(jpg_folder)
# print(f"Most common prediction: {result}")