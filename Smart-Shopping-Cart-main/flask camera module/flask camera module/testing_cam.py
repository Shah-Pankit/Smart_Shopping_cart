import cv2
import os
import time
import threading
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, Response
from flask.helpers import url_for
from flask.templating import render_template_string
from cs50 import SQL
from flask_session import Session
from datetime import timedelta
from random import randint
from new_modelprediction_image import makePredictionsForFolder
from convert_video_frame import video_convert

# Configure application
app = Flask(__name__)
app.secret_key = "bdsvjdv32543ub345"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.permanent_session_lifetime = timedelta(minutes=45)

# Global variables for video capturing
recording = False
webcam_index = 0
video_feed_thread = None
duration = 5  # Set the duration to 5 seconds

db = SQL("sqlite:///shopping_cart.db")

def generate_frames():
    global recording
    admin_video_path = "static/admin_video/"

    # Generate a random folder name
    random_folder = f"random{randint(1, 1000)}"
    video_file_path = os.path.join(admin_video_path, random_folder)

    # Ensure the folder exists
    os.makedirs(video_file_path, exist_ok=True)

    cap = cv2.VideoCapture(webcam_index)

    # Set the video resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(os.path.join(video_file_path, 'output.mp4'), fourcc, 30.0, (640, 480))

    start_time = time.time()

    while recording and (time.time() - start_time) < duration:
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
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    cap.release()
    out.release()

    # Convert the video
    convert_video_frame.video_convert()

    # Make predictions on the frames
    makePredictionsForFolder("static/admin_frames/")

    # Notify recording has stopped
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', np.zeros((480, 640, 3), np.uint8))[1].tobytes() + b'\r\n')

@app.route('/')
def index():
    start_recording
    return render_template('index.html', duration=duration)

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording, video_feed_thread

    if not recording:
        recording = True
        video_feed_thread = threading.Thread(target=generate_frames)
        video_feed_thread.start()

    return redirect(url_for('live_feed'))

@app.route('/stop_recording')
def stop_recording():
    global recording, video_feed_thread
    recording = False

    if video_feed_thread:
        video_feed_thread.join()

    return redirect(url_for('index'))

@app.route('/live_feed')
def live_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
