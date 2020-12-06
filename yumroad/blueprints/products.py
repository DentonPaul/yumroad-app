from flask import Blueprint, render_template, request, redirect, url_for

from yumroad.extensions import db
from yumroad.models import Product
from yumroad.forms import ProductForm

products = Blueprint('products', __name__)

@products.route('/')
def index():
    all_products = Product.query.all()
    return render_template('products/index.html', products=all_products)

@products.route('/<int:product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id) # get or return 404
    return render_template('products/details.html', product=product)

@products.route('/create', methods=['GET', 'POST'])
def create():
    form = ProductForm()

    if form.validate_on_submit(): # request is a POST and values are valid
        product = Product(name=form.name.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products.details', product_id=product.id))
    return render_template('products/create.html', form=form)

@products.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404

