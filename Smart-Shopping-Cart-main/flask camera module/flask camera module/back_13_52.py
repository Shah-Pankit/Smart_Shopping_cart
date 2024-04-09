from flask import Flask, render_template, Response
import cv2
import threading
import os
import time
from random import randint
import numpy as np
from convert_video_frame import video_convert
from new_modelprediction_image import makePredictionsForFolder
app = Flask(__name__)
webcam_index = 0
duration = 5  # Set your desired duration


# def generate_frames():
#     while True:
#         admin_video_path = "static/admin_video/"
#         random_folder = f"random{randint(1, 1000)}"
#         video_file_path = os.path.join(admin_video_path, random_folder)
#         os.makedirs(video_file_path, exist_ok=True)
#         cap = cv2.VideoCapture(webcam_index)
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#         fourcc = cv2.VideoWriter_fourcc(*'MP4V')
#         out = cv2.VideoWriter(os.path.join(video_file_path, 'output.mp4'), fourcc, 30.0, (640, 480))
#         start_time = time.time()
#         while (time.time() - start_time) < duration:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             out.write(frame)
#             ret, jpeg = cv2.imencode('.jpg', frame)
#             if not ret:
#                 break
#         cap.release()
#         out.release()
#         video_convert(video_file_path)
#         makePredictionsForFolder("static/admin_frames/random1/")
#         time.sleep(5)  # Wait for 5 seconds before starting the next recording

def generate_frames():
    folder_counter = 1
    while True:
        admin_video_path = "static/admin_video/"
        random_folder = f"random{folder_counter}"
        video_file_path = os.path.join(admin_video_path, random_folder)
        os.makedirs(video_file_path, exist_ok=True)
        latest_video_number = 0
        existing_files = os.listdir(video_file_path)
        for file_name in existing_files:
            if file_name.endswith('.mp4') and file_name[:-4].isdigit():
                video_number = int(file_name[:-4])
                latest_video_number = max(latest_video_number, video_number)
        next_video_number = latest_video_number + 1
        video_file_path = os.path.join(video_file_path, f'{next_video_number}.mp4')
        cap = cv2.VideoCapture(webcam_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter(video_file_path, fourcc, 30.0, (640, 480))
        start_time = time.time()
        while (time.time() - start_time) < duration:
            ret, frame = cap.read()
            if not ret:
                break
            # Write the frame to the output video file
            out.write(frame)
            # Encode the frame as JPEG for live feed
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                break
            # Yield the frame in bytes
            # yield (b'--frame\r\n'
            #     b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        cap.release()
        out.release()
        video_convert()
        # Notify recording has stopped
        # yield (b'--frame\r\n'
        #     b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', np.zeros((480, 640, 3), np.uint8))[1].tobytes() + b'\r\n')
        # imgModel = imageModel()
        folder_counter += 1
        time.sleep(5)
        pred = makePredictionsForFolder(f"static/admin_frames/random{folder_counter}/")
        print(pred)



@app.route('/')
def home():
    threading.Thread(target=generate_frames).start()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
