# importing necessary libraries
# To connect and use flask
from flask import Flask, session, redirect, url_for, jsonify, request
# To connect and use mySQL
import mysql.connector

# use for face recognition
import cv2
import pyttsx3
import pickle

# To modify and handle date and time
from datetime import datetime
# To handle sending/sharing of emails to the user
import smtplib

# Initialising the flask app
app = Flask(__name__)

# Create database connection
connection = mysql.connector.connect(user='root', password='20011013', database='facerecognition')
cursor = connection.cursor()
# app.config["DEBUG"] = True # Enable debug mode to enable hot-reloader.


'''
Description: This function is used to call face recognition programme and allow face recognition to work.
Param: None
Return: String

'''


def face_recognition():
    # 1 Get time info from user
    date = datetime.utcnow()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # 2 Load recognize and read label from model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("train.yml")

    labels = {"person_name": 1}
    path = "labels.pickle"
    with open(path, "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}

    # create text to speech
    engine = pyttsx3.init()
    rate = engine.getProperty("rate")
    engine.setProperty("rate", 175)

    # Define camera and detect face
    face_cascade = cv2.CascadeClassifier(
        'haarcascade/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    # 3 Open the camera and start face recognition
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            # predict the id and confidence for faces
            id_, conf = recognizer.predict(roi_gray)

            # If the face is recognized
            if conf >= 20:
                font = cv2.QT_FONT_NORMAL
                id = 0
                id += 1
                name = labels[id_]
                current_name = name
                color = (255, 0, 0)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1,
                            color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

                # Find the student's information in the database.
                select = "SELECT student_id, name, login_time, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Student WHERE name='%s'" % (
                    name)
                cursor.execute(select)
                result = cursor.fetchall()
                print("result: ", result)
                data = "error"

                for x in result:
                    data = x

                # If the student's information is not found in the database
                if data == "error":
                    print("The student", current_name,
                          "is NOT FOUND in the database.")
                    return ("ERROR")

                # If the student's information is found in the database
                else:
                    # Update the data in database
                    update = "UPDATE Student SET login_date=%s WHERE name=%s"
                    val = (date, current_name)
                    cursor.execute(update, val)
                    update = "UPDATE Student SET login_time=%s WHERE name=%s"
                    val = (current_time, current_name)
                    cursor.execute(update, val)
                    connection.commit()
                    print(hello)
                    engine.say(hello)
                    cap.release()
                    cv2.destroyAllWindows()
                    return result

            # If the face is unrecognized
            else:
                color = (255, 0, 0)
                stroke = 2
                font = cv2.QT_FONT_NORMAL
                cv2.putText(frame, "UNKNOWN", (x, y), font,
                            1, color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
                hello = ("Your face is not recognized")
                print(hello)
                engine.say(hello)
                return (hello)

        # cv2.imshow('Attendance System', frame)
        k = cv2.waitKey(20) & 0xff
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# A route to check if home is working
@app.route('/')
def index():
    return "Working..."

# A login route to call the face recognition function and authenticate user login and start session
@app.route("/login", methods=['GET'])
def login():
    print("Using Facial Recognition to Login...")
    # getting the data from function and checking if the person is in database or not
    result = face_recognition()
    if (result == "Your face is not recognized"):
        return {"login": "N"}
    else:
        return {
            "login": "Y",
            "id": result[0][0],
            "name": result[0][1],
            "login_time": result[0][2],
            "date": f"{result[0][3]}/{result[0][4]}/{result[0][5]}"
        }
