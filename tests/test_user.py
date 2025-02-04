from flask import url_for
import pytest

from yumroad.models import db, User

EXAMPLE_EMAIL = "test@example.com"
EXAMPLE_PASSWORD = "testtest"
STORE_NAME = "Test Store"

VALID_REGISTER_PARAMS = {
    "store_name": STORE_NAME,
    "email": EXAMPLE_EMAIL,
    "password": EXAMPLE_PASSWORD,
    "confirm": EXAMPLE_PASSWORD,
}

VALID_LOGIN_PARAMS = {
    'email': EXAMPLE_EMAIL,
    'password': EXAMPLE_PASSWORD,
}

def create_user(email=EXAMPLE_EMAIL, password=EXAMPLE_PASSWORD):
    user = User.create(email, password)
    db.session.add(user)
    db.session.commit()
    return user

# Unit Tests
def test_user_creation(client, init_database):
    assert User.query.count() == 0
    user = create_user()
    assert User.query.count() == 1
    assert user.password is not EXAMPLE_PASSWORD

# def test_email_password_validation(client, init_database):
#     assert User.query.count() == 0
#     with pytest.raises(Exception):
#         create_user('', EXAMPLE_PASSWORD)
#     with pytest.raises(Exception):
#         create_user(EXAMPLE_EMAIL, '')
#     assert User.query.count() == 0

# Functional Tests
def test_get_register(client, init_database):
    response = client.get(url_for('user.register'))
    assert response.status_code == 200
    assert 'Sign Up' in str(response.data)
    assert 'Email' in str(response.data)
    assert 'Password' in str(response.data)

def test_register(client, init_database):
    response = client.post('/register', data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registered successfully' in response.data
    assert EXAMPLE_EMAIL in str(response.data)
    assert b'Yumroad' in response.data

def test_register_invalid(client, init_database):
    invalid_data = VALID_REGISTER_PARAMS.copy()
    invalid_data['email'] = 'abc'
    response = client.post('/register', data=invalid_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email address' in response.data

def test_register_with_existing_user(client, init_database):
    user = create_user()
    response = client.post('/register', data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert b'That email already has an account' in response.data
    assert b'Registered succesfully.' not in response.data
    assert b'You are already logged in' not in response.data

def test_already_logged_in_register(client, init_database, authenticated_request):
    response = client.post('/register', data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'You are already logged in' in str(response.data)

def test_get_login(client, init_database):
    response = client.get(url_for('user.login'))
    assert response.status_code == 200
    assert 'Login' in str(response.data)
    assert 'Email' in str(response.data)
    assert 'Password' in str(response.data)

def test_login(client, init_database):
    create_user()
    response = client.post(url_for('user.login'), data=VALID_LOGIN_PARAMS, follow_redirects=True)

    assert response.status_code == 200
    assert b'Logged in successfully' in response.data

def test_already_logged_in_login(client, init_database, authenticated_request):
    response = client.post(url_for('user.login'), data=VALID_LOGIN_PARAMS, follow_redirects=True)

    assert response.status_code == 200
    assert 'You are already logged in' in str(response.data)

def test_login_invaid_email(client, init_database):
    create_user()
    response = client.post(url_for('user.login'), data=dict(
        email="test",
        password=EXAMPLE_PASSWORD
    ), follow_redirects=True)

    assert response.status_code == 200
    assert 'Invalid email address' in str(response.data)

def test_login_no_user(client, init_database):
    create_user()
    response = client.post(url_for('user.login'), data=dict(
        email="test@nonexistent.com",
        password=EXAMPLE_PASSWORD
    ), follow_redirects=True)

    assert response.status_code == 200
    assert 'Invalid email or password' in str(response.data)

def test_login_bad_password(client, init_database):
    create_user()
    response = client.post(url_for('user.login'), data=dict(
        email=EXAMPLE_EMAIL,
        password="badpassword"
    ), follow_redirects=True)

    assert response.status_code == 200
    assert 'Invalid email or password' in str(response.data)

def test_logout(client, init_database, authenticated_request):
    user = User.query.first()
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert url_for('user.login') in str(response.data)
    assert url_for('user.logout') not in str(response.data)
    assert b'Log out' not in response.data
