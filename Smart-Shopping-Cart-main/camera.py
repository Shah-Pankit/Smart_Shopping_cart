from flask import Flask, render_template, request, redirect, url_for
import cv2
import time
import threading
import sys

app = Flask(__name__)

# Global variables for video capturing
recording = False
label = ""
duration = 0
webcam_index = 0

def record_labeled_video():
    global recording

    cap = cv2.VideoCapture(webcam_index)

    # Set the video resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'{label}.avi', fourcc, 20.0, (640, 480))

    start_time = time.time()

    while recording and (time.time() - start_time) < duration:
        ret, frame = cap.read()

        # Display the label on the video
        label_text = f"Label: {label}"
        cv2.putText(frame, label_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Write the frame to the output video file
        out.write(frame)

    cap.release()
    out.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording, label, duration

    label = request.form['label']
    duration = int(request.form['duration'])

    if not recording:
        recording = True
        threading.Thread(target=record_labeled_video).start()

    return redirect(url_for('index'))

@app.route('/stop_recording')
def stop_recording():
    global recording
    recording = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
