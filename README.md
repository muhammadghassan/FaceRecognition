## This project is  released with the consent of all parties.

# 🎭 Face Recognition System  

## 📌 Overview  

This project implements a **Face Recognition System** using **OpenCV, Streamlit, and Flask**. It enables **face data collection, training, and real-time recognition** with an integrated **GUI for authentication**. The system also integrates with **MySQL** for user data management.  

---

## 🚀 Features  

✅ **Face Data Collection** – Capture and store facial images for training.  
✅ **Model Training** – Train a face recognition model using OpenCV.  
✅ **Real-time Face Recognition** – Authenticate users through a GUI interface.  
✅ **MySQL Database Integration** – Store and manage user data.  
✅ **Flask Backend** – API for handling login and authentication requests.  
✅ **Streamlit GUI** – User-friendly interface for interaction.  

---

## 📥 Installation & Setup  

### 🔧 Environment Setup  

First, create a **virtual environment** using **Anaconda**:  

```bash
conda create -n face python=3.x
conda activate face
pip install -r requirements.txt
```
## Useage

### Environment

Create virtual environment using Anaconda.
```
conda create -n face python=3.x
conda activate face
pip install -r requirements.txt
```

## Run

### 1. Face Recognition

#### 1.1 Collect Face Data
```
"""
user_name = "Jack"   # the name
NUM_IMGS = 400       # the number of saved images
"""
python face_capture.py
```
The camera will be activated and the captured images will be stored in `data/Jack` folder.      
**Note:** Only one person’s images can be captured at a time.

#### 1.2 Train a Face Recognition Model
```
python train.py
```
`train.yml` and `labels.pickle` will be created at the current folder.



### 2. Database Design

#### 2.2 Import Database
Open mysql server and import the file `facerecognition.sql`.
```
# login the mysql command
mysql -u root -p

# create database.  'mysql>' indicates we are now in the mysql command line
mysql> CREATE DATABASE facerecognition;
mysql> USE facerecognition;

# import from sql file
mysql> source facerecognition.sql
```

### 3. Login Interface

#### 3.1 OpenCV GUI
```
FLASK_APP=backend.py flask run
streamlit run gui.py
```

Once in the streamlit webpage, click on the Login button will start the facial recognition procedures.

As the facial recognition system is not very well implmented to the system, a debug button is added for development and debug purpose for the UI.
