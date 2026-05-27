---
title: PomegranateGuard
emoji: 🛡️
colorFrom: red
colorTo: green
sdk: docker
app_port: 5000
pinned: false
---

# PomegranateGuard 🛡️

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

### 1. Clone the Repository
```bash
git clone https://github.com/Prosquries/PomegranateGuard_1B.git
cd PomegranateGuard_1B
```

**Note on Models:** The trained models (`.h5` files) are now included in this repository. Note that some files (like `pomegranate_cnn.h5`) exceed 100MB and require **Git LFS** (Large File Storage) to be pushed to GitHub.

### 2. Download Missing Datasets (Optional)
The raw dataset is still hosted externally due to its size.
Download the **`dataset/`** folder from the [Google Drive Project Folder](https://drive.google.com/drive/u/1/folders/1oFR9ssk2eakVTN3HyXgg7X1zCOUfcb-F) if you plan to retrain the models.

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
*Created by [Lakshya Pareek](https://github.com/Lakshya-Pareek)*
