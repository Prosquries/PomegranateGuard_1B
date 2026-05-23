import pytest
from app import app, db, User
from flask import session

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_login_page_load(client):
    """Test if login page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_signup_page_load(client):
    """Test if signup page loads correctly."""
    response = client.get('/signup')
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_user_signup(client):
    """Test user registration."""
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Password123!'
    }, follow_redirects=True)
    assert b"Your account has been created!" in response.data

def test_user_login(client):
    """Test user login."""
    # First sign up
    client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Password123!'
    })
    
    # Then login
    response = client.post('/', data={
        'email': 'test@example.com',
        'password': 'Password123!'
    }, follow_redirects=True)
    # Check for dashboard content or specific welcome message
    assert b"Dashboard" in response.data or b"Welcome" in response.data

def test_logout(client):
    """Test user logout."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    
    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data

def test_protected_routes(client):
    """Test that protected routes redirect to login."""
    protected_urls = ['/dashboard', '/library', '/symptom-checker']
    for url in protected_urls:
        response = client.get(url, follow_redirects=True)
        assert b"Please log in to access this page" in response.data
