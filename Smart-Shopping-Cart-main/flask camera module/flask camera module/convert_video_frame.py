# import cv2
# import os

# def extract_frames(video_path, output_folder):
#     # Extract frames from the video and save them to the output folder

#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # Extract category and video name
#     category = os.path.basename(os.path.dirname(video_path))
#     video_name = os.path.splitext(os.path.basename(video_path))[0]

#     # Create or access the category folder in the output directory
#     category_output_folder = os.path.join(output_folder, category)
#     if not os.path.exists(category_output_folder):
#         os.makedirs(category_output_folder)

#     # Check if frames are already extracted from this video
#     existing_frames = set(os.listdir(category_output_folder))

#     # Open the video file
#     cap = cv2.VideoCapture(video_path)

#     # Get the frames per second (fps) and frame dimensions
#     fps = int(cap.get(cv2.CAP_PROP_FPS))

#     frame_count = 0
#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             break  # Break the loop if no more frames are available

#         # Construct the output file path
#         output_path = os.path.join(category_output_folder, f"{video_name}_frame_{frame_count}.jpg")

#         # Save the frame as a JPG image if it doesn't exist already
#         if output_path not in existing_frames:
#             cv2.imwrite(output_path, frame)
#             frame_count += 1
#     cap.release()

# def video_convert():

#     video_folder = "static/admin_video/"
#     output_folder = "static/admin_frames/"

#     for category_folder in os.listdir(video_folder):
#         if os.path.isdir(os.path.join(video_folder, category_folder)):
#             category_path = os.path.join(video_folder, category_folder)
#             for video_file in os.listdir(category_path):
#                 if video_file.endswith(".mp4"):     
#                     video_path = os.path.join(category_path, video_file)
#                     extract_frames(video_path, output_folder)

# ---------------------------------------------\
import cv2
import os

def extract_frames(video_path, output_folder):
    # Extract frames from the video and save them to the output folder

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract category and video name
    category = os.path.basename(os.path.dirname(video_path))
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Create or access the category folder in the output directory
    category_output_folder = os.path.join(output_folder, category)
    if not os.path.exists(category_output_folder):
        os.makedirs(category_output_folder)

    # Check if frames are already extracted from this video
    existing_frames = set(os.listdir(category_output_folder))

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the frames per second (fps) and frame dimensions
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break  # Break the loop if no more frames are available

        # Construct the output file path
        output_path = os.path.join(category_output_folder, f"{video_name}_frame_{frame_count}.jpg")

        # Skip if the frame already exists
        if os.path.basename(output_path) in existing_frames:
            continue

        # Save the frame as a JPG image
        cv2.imwrite(output_path, frame)
        frame_count += 1
    cap.release()

def video_convert():
    video_folder = "static/admin_video/"
    output_folder = "static/admin_frames/"

    for category_folder in os.listdir(video_folder):
        if os.path.isdir(os.path.join(video_folder, category_folder)):
            category_path = os.path.join(video_folder, category_folder)
            for video_file in os.listdir(category_path):
                if video_file.endswith(".mp4"):     
                    video_path = os.path.join(category_path, video_file)
                    extract_frames(video_path, output_folder)
