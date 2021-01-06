from flask_login import current_user
from flask import abort
import rq_dashboard

rq_blueprint = rq_dashboard.blueprint

@rq_blueprint.before_request
def authenticate(*args, **kwargs):
    if not current_user.is_authenticated:
        return abort(401)
