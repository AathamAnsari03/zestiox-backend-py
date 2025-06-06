from app.models.user import User
from app.db.database import db

def get_user_by_mobile(mobile):
    return User.query.filter_by(mobile=mobile).first()

def create_user(name, mobile, password_hash):
    user = User(name=name, mobile=mobile, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user
