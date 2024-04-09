import os
from imagemodel import imageModel
from collections import Counter

def makePredictionsForFolder(folder_path):
    imgModel = imageModel()
    predictions = []

    for image_file in os.listdir(folder_path):
        if image_file.endswith(".jpg"):
            image_path = os.path.join(folder_path, image_file)
            predictions.append(imgModel.predict_on_image(image_path))

    # Find the most common prediction
    most_common_prediction = Counter(predictions).most_common(1)
    
    if most_common_prediction:
        return most_common_prediction[0][0]
    else:
        return "No predictions."

# Example usage:
jpg_folder = r"../flask camera module/flask camera module/static/admin_frames/random2/"
result = makePredictionsForFolder(jpg_folder)   
print(f"Most common prediction: {result}")  