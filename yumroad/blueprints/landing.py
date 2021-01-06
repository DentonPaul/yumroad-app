from sqlalchemy.orm import joinedload
from flask import Blueprint, render_template
from flask_login import current_user
from yumroad.models import Store
from yumroad.extensions import cache

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/')
@cache.cached(timeout=120, unless=lambda: current_user.is_authenticated)
def index():
    # This is a bad query, optimize it later
    stores = Store.query.options(
        joinedload(Store.products)
    ).limit(3).all()
    return render_template('landing/index.html', stores=stores)