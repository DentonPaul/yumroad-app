from flask import Flask, redirect, url_for, render_template
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

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

    if app.config.get('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[FlaskIntegration(), SqlalchemyIntegration()],
            send_default_pii=True,
            traces_sample_rate=1.0
        )

    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    app.register_blueprint(products, url_prefix='/product')
    app.register_blueprint(user_bp)
    app.register_blueprint(store_bp, url_prefix='/store')
    app.register_blueprint(checkout_bp)
    app.register_blueprint(landing_bp)

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/401.html'), 401 # pragma: no cover

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500 # pragma: no cover

    return app


