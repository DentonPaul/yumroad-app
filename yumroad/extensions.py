from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate
# from flask_mail import Mail
from flask_assets import Environment
from sqlalchemy import MetaData
from flask_rq2 import RQ
from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache

from yumroad.payments import Checkout

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate() 
# mail = Mail()
checkout = Checkout()
assets_env = Environment()
rq2 = RQ()
debug_toolbar = DebugToolbarExtension()
cache = Cache()