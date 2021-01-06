from flask import Flask, redirect, url_for

from yumroad.blueprints.products import products
from yumroad.blueprints.users import user_bp
from yumroad.blueprints.stores import store_bp
from yumroad.blueprints.checkout import checkout_bp
from yumroad.blueprints.landing import landing_bp
from yumroad.config import configurations
from yumroad.extensions import (db, csrf, login_manager, migrate, checkout, assets_env) #mail

from webassets.loaders import PythonLoader as PythonAssetsLoader
from yumroad import assets

def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    # mail.init_app(app)
    checkout.init_app(app)
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    app.register_blueprint(products, url_prefix='/product')
    app.register_blueprint(user_bp)
    app.register_blueprint(store_bp, url_prefix='/store')
    app.register_blueprint(checkout_bp)
    app.register_blueprint(landing_bp)

    return app


