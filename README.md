

```markdown
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

Ensure that you have **MySQL** installed and running.  

---

## 🔄 Usage  

### 1️⃣ Face Recognition  

#### 1.1 📸 Collect Face Data  

To capture images for a user, edit the following parameters in **`face_capture.py`**:  

```python
user_name = "Jack"   # Name of the person
NUM_IMGS = 400       # Number of images to capture
```

Then, run:  

```bash
python face_capture.py
```

- The camera will be activated to capture images.  
- Images will be stored in the **`data/Jack/`** folder.  
- **Note:** Only one person’s images can be captured at a time.  

---

#### 1.2 🏋️ Train the Face Recognition Model  

After collecting face data, train the model by running:  

```bash
python train.py
```

This will generate:  
✅ `train.yml` – Stores the trained model data.  
✅ `labels.pickle` – Maps label names to face IDs.  

---

### 2️⃣ Database Setup  

#### 2.1 📂 Import Database  

1. **Start MySQL Server**  
2. **Login to MySQL:**  

```bash
mysql -u root -p
```

3. **Create the database:**  

```sql
CREATE DATABASE facerecognition;
USE facerecognition;
```

4. **Import the SQL file:**  

```sql
source facerecognition.sql;
```

- This will initialize the database schema.  

---

### 3️⃣ Login Interface  

#### 3.1 🖥️ OpenCV GUI  

Start the **Flask backend** and **Streamlit GUI** with:  

```bash
FLASK_APP=backend.py flask run
streamlit run gui.py
```

- The **GUI login page** will open in a browser.  
- Click **Login** to start facial recognition.  
- A **debug button** is available for **testing and development**.  

---

## 🛠️ Project Structure  

```
📂 FaceRecognition/
│── 📂 data/                  # Captured face images
│── 📂 models/                # Trained models
│── 📂 static/                # UI assets (CSS, JS)
│── 📂 templates/             # HTML templates for Flask
│── ├── backend.py            # Flask backend server
│── ├── gui.py                # Streamlit GUI interface
│── ├── train.py              # Model training script
│── ├── face_capture.py       # Face data collection script
│── ├── facerecognition.sql   # Database schema
│── ├── requirements.txt      # Dependencies list
│── ├── README.md             # Project documentation
```

---

## 📜 License  

This project is licensed under the **MIT License**. See `LICENSE` for details.  

---

## 👨‍💻 Contributors  

- **Muhammad Ghassan Jawwad**  


---

## 🛠 Future Improvements  

📌 **Improve Model Accuracy** – Use advanced ML models like CNNs.  
📌 **Multi-user Recognition** – Identify multiple faces in a single frame.  
📌 **Mobile App Integration** – Allow login via smartphone camera.  
📌 **2FA Authentication** – Enhance security with multi-factor authentication.  

---

💡 **Feel free to contribute or raise issues for improvements!** 🚀  
```

---
