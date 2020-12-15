from werkzeug.security import generate_password_hash
from sqlalchemy.orm import validates
from yumroad.extensions import db
from flask_login import UserMixin

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(120), nullable = True)

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError("Needs to have a real name")
        return name

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(225), nullable=False)
    password = db.Column(db.String(225), nullable=False)

    @classmethod
    def create(cls, email, password):
        """ Usage: User.create('test@example.com', 'example')
        """
        hashed_password = generate_password_hash(password)
        return User(email=email.lower().strip(), password=hashed_password)
