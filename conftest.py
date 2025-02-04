import pytest

from flask import url_for

from yumroad import create_app
from yumroad.extensions import db
from yumroad.models import User, Store, Product

@pytest.fixture
def app():
    return create_app('test')

@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()

@pytest.fixture
def authenticated_request(client):
    new_user = User.create('test@example.com', 'examplepass')
    store = Store(name="Test Store", user=new_user)
    db.session.add(new_user)
    db.session.commit()

    response = client.post(url_for('user.login'), data={
        'email': 'test@example.com',
        'password': 'examplepass'
    }, follow_redirects=True)
    yield client

@pytest.fixture
def user_with_product():
    new_user = User.create("test@example.com", "pass")
    store = Store(name="Test Store", user=new_user)
    product = Product(name='Test Product', description='a product', store=store)
    db.session.add(product)
    db.session.commit()
    yield new_user