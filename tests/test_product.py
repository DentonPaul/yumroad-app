from flask import url_for
import pytest
import vcr
from yumroad.extensions import db
from yumroad.models import Product, Store, User

@pytest.fixture
def sample_book():
    new_user = User.create('store@example.com', 'examplepass')
    db.session.add(new_user)
    store = Store(name='Store Name', user=new_user)
    # db.session.add(store)
    book = Product(name="Sherlock Homes", store=store,
                    description="A house hunting detective")
    db.session.add(book)
    db.session.commit()
    return book

def test_product_creation(client, init_database, authenticated_request):
    assert Product.query.count() == 0
    book = Product(name='Sherlock Homes', description='A house hunting detective')
    db.session.add(book)
    db.session.commit()
    assert Product.query.count() == 1
    assert Product.query.first().name == book.name

def test_name_validation(client, init_database):
    with pytest.raises(ValueError):
        Product(name='    a', description='invalid book')
        
def test_index_page(client, init_database, sample_book):
    response = client.get(url_for('products.index'))
    assert response.status_code == 200
    assert 'Yumroad' in str(response.data)
    assert sample_book.name in str(response.data)

    expected_link = url_for('products.details', product_id=sample_book.id)
    assert expected_link in str(response.data)

@vcr.use_cassette('tests/cassettes/new_stripe_session.yaml',
                  filter_headers=['authorization'], record_mode='once') # vcr not working
def test_details_page(client, init_database, sample_book):
    response = client.get(url_for('products.details', product_id=sample_book.id))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert b'See more products' in response.data

def test_not_found(client, init_database):
    response = client.get(url_for('products.details', product_id=1))
    assert response.status_code == 404
    assert url_for('products.index') in str(response.data)

def test_new_page(client, init_database, authenticated_request):
    response = client.get(url_for('products.create'))

    assert response.status_code == 200
    assert b'Name' in response.data
    assert b'Create' in response.data

def test_new_page_unauth(client, init_database):
    response = client.get(url_for('products.create'))

    assert response.status_code == 302
    assert response.location == url_for('user.login', _external=True)

def test_creation(client, init_database, authenticated_request):
    response = client.post(url_for('products.create'),
                            data=dict(name='Test Product', description='is persisted'),
                            follow_redirects=True)

    assert response.status_code == 200
    assert b'Sold out' in response.data

def test_invalid_creation(client, init_database, authenticated_request):
    response = client.post(url_for('products.create'),
                            data=dict(name='ab', description='is not valid'),
                            follow_redirects=True)
    assert response.status_code == 200
    assert b'is not valid' in response.data
    assert b'Field must be between' in response.data
    assert b'is-invalid' in response.data

def test_edit_page(client, init_database, sample_book, authenticated_request):
    response = client.get(url_for('products.edit', product_id=sample_book.id))
    assert response.status_code == 200
    assert sample_book.description in str(response.data)
    assert sample_book.name in str(response.data)
    assert b'Edit' in response.data

def test_edit_submission(client, init_database, sample_book, authenticated_request):
    old_description = sample_book.description
    old_name = sample_book.name
    response = client.post(url_for('products.edit', product_id=sample_book.id),
                            data={'name': 'test-change', 'description': 'is persisted'},
                            follow_redirects=True)
    assert response.status_code == 200
    assert 'test-change' in str(response.data)
    assert 'is persisted' in str(response.data)
    assert old_description not in str(response.data)
    assert old_name not in str(response.data)
    assert b'Edit' not in response.data

def test_invalid_edit_submission(client, init_database, sample_book, authenticated_request):
    old_description = sample_book.description
    old_name = sample_book.name
    response = client.post(url_for('products.edit', product_id=sample_book.id),
                            data=dict(name='br0', description='is persisted'),
                            follow_redirects=True)
    assert response.status_code == 200
    assert b'br0' in response.data
    assert b'Field must be between 4 and 60 characters long' in response.data
    assert Product.query.get(sample_book.id).description == old_description
    assert old_description not in str(response.data)
    assert old_name in str(response.data) # It's still in the page title
    assert b'Edit' in response.data




