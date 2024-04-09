from imagemodel import imageModel
from video_to_frames import extract_frames
import os
# import ssl 
# ssl._create_default_https_context = ssl._create_unverified_context

def makePrediction(video_path):
    # Extract frames from the video
    output_folder = "./dataset_frames/"
    extract_frames(video_path, output_folder)

    # Predict on the extracted frames
    imgModel = imageModel()
    
    # Assuming you want to predict on a frame from the video
    frame_path = os.path.join(output_folder, "frame_0.jpg")
    prediction = imgModel.predict_on_image(frame_path)
    
    print("Prediction:", prediction)

# Placeholder way to load video
video_path = "../prediction/vid/APPLES/"  # Update the path to your video
makePrediction(video_path)
