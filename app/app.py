import os
import logging
import re
from functools import wraps
import numpy as np
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = app.logger

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'pomegranate_guard_secret_key_123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database path setup
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "instance", "site.db")

# Safety Check: If we can't write to the instance folder, use /tmp
if not os.access(os.path.dirname(db_path), os.W_OK):
    logger.warning("Instance folder not writable, falling back to /tmp/site.db")
    db_path = "/tmp/site.db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Ensure database and test user
try:
    with app.app_context():
        db.create_all()
        test_email = "admin@test.com"
        if not User.query.filter_by(email=test_email).first():
            hashed_pw = generate_password_hash("Admin@123")
            test_user = User(username="admin", email=test_email, password=hashed_pw)
            db.session.add(test_user)
            db.session.commit()
            logger.info("TEST USER READY: admin@test.com")
except Exception as e:
    logger.error(f"Critical Database Error: {e}")

@app.route('/debug-db')
def debug_db():
    users = User.query.all()
    return {"user_count": len(users), "emails": [u.email for u in users]}

# Lazy model loading
_model = None

def get_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), "model/pomegranate_final_model.h5")
        _model = load_model(model_path)
    return _model

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        
        if not re.match(email_regex, email):
            flash('Invalid email address.', 'danger')
            return redirect(url_for('signup'))
            
        if not re.match(password_regex, password):
            flash('Password must be at least 8 characters, and include a number and a special character.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Email or Username already exists.', 'danger')
            
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/library')
@login_required
def library():
    return render_template("disease_library.html")

@app.route('/predict', methods=['POST'])
@login_required
def predict():

    file = request.files['file']

    if file.filename == '':
        return redirect('/dashboard')

    # SAVE FILE
    filename = file.filename

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )

    file.save(filepath)

    # PREPROCESS IMAGE
    img = image.load_img(filepath, target_size=(224,224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # PREDICTION
    prediction = get_model().predict(img_array)

    confidence = round(np.max(prediction) * 100, 2)

    class_index = np.argmax(prediction)

    classes = [
        "Healthy",
        "Bacterial Blight",
        "Anthracnose",
        "Fruit Rot"
    ]

    disease = classes[class_index]

    # DISEASE DETAILS (EXPANDED)
    disease_info = {

        "Healthy": {
            "description": "Status: Healthy. The fruit/leaf shows no visible signs of pathogenic infections or physiological disorders. The skin is firm and the color is natural for its ripening stage.",
            "prevention": "Continue standard cultural practices. Maintain proper irrigation scheduling, ensure adequate sunlight, and perform routine nutrient management to keep the plant immunity high.",
            "severity": "low"
        },

        "Bacterial Blight": {
            "description": "Scientific Name: Xanthomonas axonopodis pv. punicae. \nSymptoms: Appears as water-soaked, dark, irregular spots on leaves and fruits. As it progresses, the spots turn into black oily lesions. Severe infections lead to deep cracking of the fruit, making it unmarketable, and cause premature leaf drop.",
            "prevention": "Treatment: Spray Streptomycin sulphate or Copper oxychloride immediately. \nPrevention: Prune and destroy infected branches far from the orchard. Avoid overhead irrigation and ensure farm tools are sanitized between uses.",
            "severity": "high"
        },

        "Anthracnose": {
            "description": "Scientific Name: Colletotrichum gloeosporioides. \nSymptoms: Characterized by small, regular or irregular, black sunken spots on the fruit. Over time, these spots can coalesce and cause significant rotting. On leaves, it causes yellowing and premature dropping.",
            "prevention": "Treatment: Apply fungicides such as Mancozeb, Propiconazole, or Carbendazim. \nPrevention: Improve canopy ventilation by pruning dense foliage. Remove and burn fallen infected fruits and leaves to reduce the fungal inoculum.",
            "severity": "medium"
        },

        "Fruit Rot": {
            "description": "Pathogen: Various fungi including Alternaria, Aspergillus, or Penicillium species. \nSymptoms: Begins as a soft, watery rot, usually starting from the calyx or a wound. The internal arils decay, and fuzzy fungal growth (white, gray, or black) often appears on the surface or inside the cracked fruit.",
            "prevention": "Treatment: Spray systemic fungicides during the flowering and fruit setting stages. \nPrevention: Prevent insect damage and mechanical injuries to the fruit, which serve as entry points. Ensure proper drainage to avoid high humidity around the lower canopy.",
            "severity": "high"
        }
    }

    result = disease_info[disease]

    image_path = "uploads/" + filename

    return render_template(
        'analysis.html',
        prediction=disease,
        confidence=confidence,
        description=result['description'],
        prevention=result['prevention'],
        severity=result['severity'],
        image_path=image_path
    )

@app.route('/symptom-checker')
@login_required
def symptom_checker():
    return render_template('symptom_checker.html')

@app.route('/text-predict', methods=['POST'])
@login_required
def text_predict():
    user_text = request.form.get('symptoms', '').lower()
    
    # Simple Keyword Matching Logic
    blight_keywords = ['oil', 'water-soaked', 'crack', 'black spot', 'lesion', 'dark spot', 'bacterial']
    anthracnose_keywords = ['sunken', 'yellow', 'drop', 'rot', 'irregular spot']
    rot_keywords = ['soft', 'watery', 'fuzz', 'white growth', 'gray growth', 'decay', 'smell', 'fungus']
    
    prediction = "Healthy"
    confidence = 0.0
    
    # Score the input based on keywords
    scores = {"Bacterial Blight": 0, "Anthracnose": 0, "Fruit Rot": 0}
    
    for word in blight_keywords:
        if word in user_text: scores["Bacterial Blight"] += 1
    for word in anthracnose_keywords:
        if word in user_text: scores["Anthracnose"] += 1
    for word in rot_keywords:
        if word in user_text: scores["Fruit Rot"] += 1
        
    max_score_disease = max(scores, key=scores.get)
    if scores[max_score_disease] > 0:
        prediction = max_score_disease
        confidence = min(round((scores[max_score_disease] / 3) * 100, 2) + 40.0, 95.0) # Mock confidence based on keyword hits
    else:
        confidence = 99.0 # Confident it's healthy if no keywords match
        
    # DISEASE DETAILS (EXPANDED)
    disease_info = {
        "Healthy": {
            "description": "Status: Healthy or Unknown. Based on your description, we couldn't confidently identify a major disease. Please monitor closely.",
            "prevention": "Maintain standard practices. If symptoms worsen, please use the Image Scanner for a better diagnosis.",
            "severity": "low"
        },
        "Bacterial Blight": {
            "description": "Scientific Name: Xanthomonas axonopodis pv. punicae. \nSymptoms: Dark oily lesions, cracking of fruit.",
            "prevention": "Treatment: Spray Streptomycin sulphate or Copper oxychloride. Prevent by pruning infected branches.",
            "severity": "high"
        },
        "Anthracnose": {
            "description": "Scientific Name: Colletotrichum gloeosporioides. \nSymptoms: Black sunken spots, yellowing of leaves.",
            "prevention": "Treatment: Apply fungicides like Mancozeb. Improve canopy ventilation.",
            "severity": "medium"
        },
        "Fruit Rot": {
            "description": "Pathogen: Fungal species (Alternaria, Aspergillus). \nSymptoms: Soft, watery rot, often with fungal growth.",
            "prevention": "Treatment: Fungicides. Prevent by avoiding mechanical injuries to fruit.",
            "severity": "high"
        }
    }
    
    result = disease_info[prediction]
    
    return render_template(
        'analysis.html',
        prediction=prediction,
        confidence=confidence,
        description=result['description'],
        prevention=result['prevention'],
        severity=result['severity'],
        image_path=None # No image for text prediction
    )

if __name__ == "__main__":
    app.run(debug=True)