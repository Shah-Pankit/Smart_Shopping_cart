from flask import Flask, render_template, Response, redirect
import cv2
import threading
import os
import time
from random import randint
import numpy as np
from convert_video_frame import video_convert
import new_modelprediction_image
from new_modelprediction_image import makePredictionsForFolder
app = Flask(__name__)
webcam_index = 0
# duration = 5  # Set your desired duration
products = None

# def generate_frames():
#     global products
#     folder_counter = 1
#     while True:
#         admin_video_path = "static/admin_video/"
#         random_folder = f"random{folder_counter}"
#         video_file_path = os.path.join(admin_video_path, random_folder)
#         os.makedirs(video_file_path, exist_ok=True)
#         latest_video_number = 0
#         existing_files = os.listdir(video_file_path)
#         for file_name in existing_files:
#             if file_name.endswith('.mp4') and file_name[:-4].isdigit():
#                 video_number = int(file_name[:-4])
#                 latest_video_number = max(latest_video_number, video_number)
#         next_video_number = latest_video_number + 1
#         video_file_path = os.path.join(video_file_path, f'{next_video_number}.mp4')
#         cap = cv2.VideoCapture(webcam_index)
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#         fourcc = cv2.VideoWriter_fourcc(*'MP4V')
#         out = cv2.VideoWriter(video_file_path, fourcc, 10.0, (640, 480))
#         duration=1
#         while duration <= 5:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             # Write the frame to the output video file
#             out.write(frame)
#             # Encode the frame as JPEG for live feed
#             ret, jpeg = cv2.imencode('.jpg', frame)
#             if not ret:
#                 break
#             duration+=1
#             # Yield the frame in bytes
#             # yield (b'--frame\r\n'
#             #     b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
#         cap.release()
#         out.release()
#         video_convert()
#         # Notify recording has stopped
#         # yield (b'--frame\r\n'
#         #     b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', np.zeros((480, 640, 3), np.uint8))[1].tobytes() + b'\r\n')
#         # imgModel = imageModel()
#         global products
#         products = makePredictionsForFolder(f"static/admin_frames/random{folder_counter}/")
#         # print("Back pred", products)
#         folder_counter += 1
#         time.sleep(1)
        

def generate_frames():
    global products
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
        out = cv2.VideoWriter(video_file_path, fourcc, 10.0, (640, 480))
        start_time = time.time()
        while (time.time() - start_time) <= 2:  # Adjust the duration here (4 seconds in this example)
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
        global products
        products = makePredictionsForFolder(f"static/admin_frames/random{folder_counter}/")
        # print("Back pred", products)
        folder_counter += 1
        time.sleep(1)

@app.route('/')
def home():
    threading.Thread(target=generate_frames).start()
    return redirect("/home")

# @app.route("/call_home")
# def call_home():
#     threading.Thread(target=index).start()
#     return redirect("/home")
    
@app.route("/home")
def index():
    global products
    while True:
        if products is not None:
            duplicate_product=set(products)
            products = list(duplicate_product)
            print("If data", products)
            return render_template("index.html", data = products)
        else:
            time.sleep(1)
            # print(products)
            return render_template("index.html", data=None)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)

