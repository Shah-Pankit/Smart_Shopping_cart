from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No image part"

    image = request.files['image']
    label = request.form['label']

    if image.filename == '':
        return "No selected image"

    if image:
        # Use the label as the filename and save the image to the server
        filename = label + os.path.splitext(image.filename)[1]  # Maintain the original file extension
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Additional logic to save label and image information to your dataset

        return "Image uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True)
