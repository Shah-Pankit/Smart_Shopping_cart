import io
from flask import Flask, render_template, request, redirect, url_for, Response
import cv2
import time
import threading
import numpy as np
import os
from cs50 import SQL
from flask import Flask, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from datetime import timedelta
import convert_video_frame
from new_imagemodel import imageModel
from new_modelprediction_image import makePredictionsForFolder
# Configure application
from datetime import timedelta
app = Flask(__name__)
app.secret_key = "bdsvjdv32543ub345"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.permanent_session_lifetime = timedelta(minutes=45)

db = SQL("sqlite:///shopping_cart.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# @app.route("/", methods=["GET", "POST"])
# def welcome():
#     if session.get("is_login") == True:
#         return redirect("/home")
#     else:
#         return render_template("welcome.html") --change file name to your opening



@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    """Log user in"""
    # This try and except block check if any person is already logged in
    if session.get("is_login") == True:
        return redirect("/home")
    else:
        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":
            email = request.form.get("email").strip().lower()
            password = request.form.get("password").strip()
            # Ensure required fields are submitted
            if email == "" and password == "":
                return render_template("faculty_signin.html", message="Please Provide All Required Details")

            # Ensure Email was submitted
            if not email:
                return render_template("faculty_signin.html", message="Please Provide Email")

            # Ensure password was submitted
            if not password:
                return render_template("faculty_signin.html", message="Please enter a password")

            # Query database for username
            try:
                rows = db.execute(
                    "SELECT * FROM faculty_details WHERE email = ?", email)
                if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
                    return render_template("faculty_signin.html", message="Incorrect email or password!")
            except Exception as e:
                print("Exception in login",e)
                return render_template("faculty_signin.html", message="Something went wrong!")
            
            # Remember which user and other detail of user has logged in
            session['is_login'] = True
            session["email"] = rows[0]["email"]
            session["uid"] = rows[0]["id"]
            session["name"] = rows[0]["fullname"]
            session["phone"] = rows[0]["phone_number"]
            session["clg_name"] = rows[0]["clg_name"]
            session["clg_gtu_code"] = rows[0]["clg_gtu_code"]

            # Redirect user to home page and executes the query
            return redirect("/home")

        # User reached route via GET (as by clicking a link or via redirect)
        else:
            return render_template("admin_login.html")


# Below is uer login
@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    """Log user in"""
    # This try and except block check if any person is already logged in
    if session.get("is_login") == True:
        return redirect("/home")
    else:
        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":
            email = request.form.get("email").strip().lower()
            password = request.form.get("password").strip()
            # Ensure required fields are submitted
            if email == "" and password == "":
                return render_template("faculty_signin.html", message="Please Provide All Required Details")

            # Ensure Email was submitted
            if not email:
                return render_template("faculty_signin.html", message="Please Provide Email")

            # Ensure password was submitted
            if not password:
                return render_template("faculty_signin.html", message="Please enter a password")

            # Query database for username
            try:
                rows = db.execute(
                    "SELECT * FROM faculty_details WHERE email = ?", email)
                if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
                    return render_template("faculty_signin.html", message="Incorrect email or password!")
            except Exception as e:
                print("Exception in login",e)
                return render_template("faculty_signin.html", message="Something went wrong!")
            
            # Remember which user and other detail of user has logged in
            session['is_login'] = True
            session["email"] = rows[0]["email"]
            session["uid"] = rows[0]["id"]
            session["name"] = rows[0]["fullname"]
            session["phone"] = rows[0]["phone_number"]
            session["clg_name"] = rows[0]["clg_name"]
            session["clg_gtu_code"] = rows[0]["clg_gtu_code"]

            # Redirect user to home page and executes the query
            return redirect("/home")

        # User reached route via GET (as by clicking a link or via redirect)
        else:
            return render_template("admin_login.html")
        
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id if found
    try:
        session.clear()
    except:
        pass
    # Redirect user to login form
    return redirect("/")


@app.route("/admin_signup", methods=["POST", "GET"])
def admin_signup():
    ''' Signup Page '''
    # Check if user is already logged in
    if session.get("admin_login") == True:
        return redirect("/home")
    else:
        if request.method == "POST":
            name = request.form.get("name").title().strip()
            password = request.form.get("password").title().strip()
            email = request.form.get("email").lower().strip()
            phone_no = request.form.get("phone")

            print(name, email, phone_no, password)

            # User input validation
            if name == "" and email == "" and password == "" and phone_no == "":
                return render_template("faculty_signup.html", message="Please Enter All Required Details")

            elif not name:
                return render_template("faculty_signup.html", message="Please Enter Name")

            elif not email:
                return render_template("faculty_signup.html", message="Please Enter An Email")

            elif not phone_no:
                return render_template("faculty_signup.html", message="Please Enter Your Phone No")

            elif not password:
                return render_template("faculty_signup.html", message="Please Enter Gtu College Code")

            hash = generate_password_hash(password)
            try:
                rows = db.execute("SELECT * FROM admin_login")
                user_already_email = []
                for row in rows:
                    user_already_email.append(row["email"])
                if email in user_already_email:
                    return render_template("faculty_signup.html", message=f'The email "{email}" is already registered kindly use another email')
            except Exception as e:
                print("Exception 1 in Signup", e)
                return render_template("faculty_signup.html", message="Something went wrong!")
            # Try to insert values in the database
            else:
                try:
                    db.execute("INSERT INTO admin_login (name, email, password, phone) VALUES (?, ?, ?, ?)",
                            name, email, hash, phone_no)
                    print("Signup Sucess")
                    flash("Signup Succes! Credentials has been sent to your Registered Email", "success")
                    return redirect("/admin_login")
                except Exception as e:
                    print("Exception 4 in Signup", e)
                    return render_template("faculty_signup.html", message="Problem occured with sending email")

        else:
            return render_template("faculty_signup.html")


@app.route("/user_signup", methods=["POST", "GET"])
def user_signup():
    ''' Signup Page '''
    # Check if user is already logged in
    if session.get("user_login") == True:
        return redirect("/home")
    else:
        if request.method == "POST":
            name = request.form.get("name").title().strip()
            address = request.form.get("address").title().strip()
            pin_code = request.form.get("pin_code").title().strip()
            wallet = request.form.get("wallet").title().strip()
            password = request.form.get("password").title().strip()
            email = request.form.get("email").lower().strip()
            phone_no = request.form.get("phone")

            print(name, email, phone_no, password, address, pin_code, wallet)

            # User input validation
            if name == "" and email == "" and password == "" and phone_no == "" and address == "" and wallet == "" and pin_code == "":
                return render_template("faculty_signup.html", message="Please Enter All Required Details")

            elif not name:
                return render_template("faculty_signup.html", message="Please Enter Name")

            elif not email:
                return render_template("faculty_signup.html", message="Please Enter An Email")

            elif not phone_no:
                return render_template("faculty_signup.html", message="Please Enter Your Phone No")

            elif not address:
                return render_template("faculty_signup.html", message="Please Enter Gtu College Code")
            elif not password:
                return render_template("faculty_signup.html", message="Please Enter Gtu College Code")
            elif not wallet:
                return render_template("faculty_signup.html", message="Please Enter Gtu College Code")
            elif not pin_code:
                return render_template("faculty_signup.html", message="Please Enter Gtu College Code")

            hash = generate_password_hash(password)
            try:
                rows = db.execute("SELECT * FROM user_login")
                user_already_email = []
                for row in rows:
                    user_already_email.append(row["email"])
                if email in user_already_email:
                    return render_template("faculty_signup.html", message=f'The email "{email}" is already registered kindly use another email')
            except Exception as e:
                print("Exception 1 in Signup", e)
                return render_template("faculty_signup.html", message="Something went wrong!")
            # Try to insert values in the database
            else:
                try:
                    db.execute("INSERT INTO user_login (name, email, password, phone, wallet, address, pin_code) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            name, email, password, phone_no, wallet, address, pin_code)
                    print("Signup Sucess")
                    flash("Signup Succes! Credentials has been sent to your Registered Email", "success")
                    return redirect("/user_login")
                except Exception as e:
                    print("Exception 4 in Signup", e)
                    return render_template("faculty_signup.html", message="Problem occured with sending email")

        else:
            return render_template("faculty_signup.html")



@app.route("/admin_video", methods=["POST", "GET"])
def admin_video():
    ''' Signup Page '''
    # Check if user is already logged in
    if not session.get("admin_login"):
        flash("Please Login First","danger")
        return redirect("/admin_login")
    else:
        if request.method == "POST":
            product_name = request.form.get("product_name").title().strip()
            company_name = request.form.get("company_name").title().strip()

            admin_video_path = os.path.join(os.getcwd(), '../static/admin_video/')  
            admin_video_folder_path = os.path.join(admin_video_path, product_name)

            admin_frames_path = os.path.join(os.getcwd(), '../static/admin_frames/')  
            admin_frames_folder_path = os.path.join(admin_frames_path, product_name)

            user_image = request.files['photo_id']

            user_product_path = os.path.join(os.getcwd(), '../static/user_product/')  
            user_folder_path = os.path.join(user_product_path, user_image.filename)

            print("User path",user_folder_path)
            print("Admin video path", admin_frames_folder_path)
            print("Admin frames path", admin_frames_folder_path)
            
            # User input validation
            if product_name == "" and company_name == "" and user_image == None:
                return render_template("student_signup.html", message="Please Enter All Required Details")
            elif not product_name:
                return render_template("student_signup.html", message="Please Enter All Required Details")
            elif not company_name:
                return render_template("student_signup.html", message="Please Enter All Required Details")
            elif not user_image:
                return render_template("student_signup.html", message="Please Enter All Required Details")
            # Try to insert values in the database
            try:
                # db.execute('INSERT INTO product_master (product_name, company_name, user_product_path, admin_video_path, admin_frames_path) VALUES (?, ?, ?, ?, ?)',
                #         product_name, company_name, user_product_path, admin_video_path, admin_frames_path)
                print("Student added success")
                flash("Student Added Successfully","success")
                return redirect("/home")
            except Exception as e:
                print("Exception in Adding Student 2", e)
                return render_template("student_signup.html")
        else:
            products = db.execute("SELECT id, product_name, company_name FROM product_master") 
            return render_template("student_signup.html", products=products)



# Below is your code
# Global variables for video capturing
recording = True
webcam_index = 0
video_feed_thread = None
duration = 5 # Set the duration to 20 seconds

def generate_frames(label):
    global recording

    admin_video_path = os.path.join('static/admin_video/')  
    admin_video_folder_path = os.path.join(admin_video_path, label)

    admin_frames_path = os.path.join('static/admin_frames/')  
    admin_frames_folder_path = os.path.join(admin_frames_path, label)

    # user_image = request.files['photo_id']

    # user_product_path = os.path.join(os.getcwd(), '../static/user_product/')  
    # user_folder_path = os.path.join(user_product_path, user_image.filename)

    # Create the folder if it doesn't exist
    os.makedirs(admin_video_folder_path, exist_ok=True)

    # Find the latest video file number in the folder
    latest_video_number = 0
    existing_files = os.listdir(admin_video_folder_path)
    for file_name in existing_files:
        if file_name.endswith('.mp4') and file_name[:-4].isdigit():
            video_number = int(file_name[:-4])
            latest_video_number = max(latest_video_number, video_number)

    # Define the video file path inside the folder with the next sequential number
    next_video_number = latest_video_number + 1
    video_file_path = os.path.join(admin_video_folder_path, f'{next_video_number}.mp4')
    cap = cv2.VideoCapture(webcam_index)

    # Set the video resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(video_file_path, fourcc, 30.0, (640, 480))

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

    print("Last admin_video_path", admin_video_folder_path)
    print("Last admin_frames_path", admin_frames_folder_path)

    convert_video_frame.video_convert()

    # Notify recording has stopped
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', np.zeros((480, 640, 3), np.uint8))[1].tobytes() + b'\r\n')
    # imgModel = imageModel()



@app.route('/')
def index():
    return render_template('camera.html', duration=duration)

@app.route('/start_recording', methods=['GET', 'POST'])
def start_recording():
    global recording, video_feed_thread

    label = request.form['label']

    if not recording:
        recording = True
        video_feed_thread = threading.Thread(target=generate_frames, args=(label,))
        video_feed_thread.start()

    return redirect(url_for('live_feed', label=label))

@app.route('/stop_recording')
def stop_recording():
    global recording, video_feed_thread
    recording = False

    if video_feed_thread:
        video_feed_thread.join()

    return redirect(url_for('index'))

@app.route('/live_feed')
def live_feed():
    label = request.args.get('label', 'default_label')
    return Response(generate_frames(label), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/livefeed')
def livefeed():
    return "This is the /livefeed route"

if __name__ == '__main__':
    app.run(debug=True)
