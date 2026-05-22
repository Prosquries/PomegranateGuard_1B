# PomegranateGuard 🍎🛡️

PomegranateGuard is a deep learning-based Full-Stack Web Application designed to detect and diagnose diseases in pomegranate fruits and leaves. Using a combination of Convolutional Neural Networks (CNN) and Transformers, the system provides high-accuracy diagnosis for common pomegranate ailments.

## 🚀 Features
*   **Image Detection:** Upload a photo of a fruit or leaf to get an instant diagnosis.
*   **Symptom Checker:** Text-based analysis using natural language symptoms.
*   **Disease Library:** Information on symptoms, prevention, and treatments for common diseases.
*   **Secure Auth:** Built-in user registration and login system.

## 🛠️ Technical Stack
*   **Frontend:** HTML5, CSS3, JavaScript
*   **Backend:** Flask (Python)
*   **Database:** SQLite (SQLAlchemy)
*   **AI Engine:** TensorFlow / Keras
*   **Models:** CNN, Hybrid HBO-optimized models, and Transformers.

---

## 📥 Prerequisites & Setup

Due to GitHub's file size limits, the large dataset and trained models are **not included** in this repository. You must download them manually to run the application.

### 1. Clone the Repository
```bash
git clone https://github.com/Prosquries/PomegranateGuard_1B.git
cd PomegranateGuard_1B
```

### 2. Download Missing Assets
Download the following folders from the [Google Drive Project Folder](https://drive.google.com/drive/u/1/folders/1oFR9ssk2eakVTN3HyXgg7X1zCOUfcb-F):
1.  **`model/`**: Required to run the application.
2.  **`dataset/`**: Required only if you plan to retrain the models.

Place the `model/` and `dataset/` folders in the root of the project directory.

### 3. Environment Setup (Linux/macOS)
It is highly recommended to use Python 3.12.

```bash
cd app
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt - For Linux

python -m pip install -r requirements.txt - For Windows
```

### 4. Link the Models
The application expects the models to be accessible within the `app` directory:
```bash
ln -s ../model ./model
```

### 5. Run the Application
```bash
python app.py
```
Access the app at: **`http://127.0.0.1:5000`**

---

## 📊 Dataset & Evaluation
The project includes a comprehensive evaluation suite. You can find classification reports, confusion matrices, and training curves in the `evaluation/` directory.

## 📜 License
This project is for educational and research purposes.

---
*Created by [Lakshya Pareek](https://github.com/Lakshya-Pareek-1)*
