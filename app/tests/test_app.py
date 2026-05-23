import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_login_page(client):
    """Test that the login page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"login" in response.data.lower()

def test_signup_page(client):
    """Test that the signup page loads."""
    response = client.get('/signup')
    assert response.status_code == 200
    assert b"signup" in response.data.lower() or b"create" in response.data.lower()
