from flask import Blueprint, request, jsonify
from app.schemas.user import UserRegisterSchema, UserSchema
from app.crud.user import get_user_by_mobile, create_user
import bcrypt

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    schema = UserRegisterSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({'error': 'Invalid input', 'details': errors}), 400

    name = data['name']
    mobile = data['mobile']
    password = data['password']

    if get_user_by_mobile(mobile):
        return jsonify({'error': 'Mobile number already registered'}), 400

    # Use bcrypt for password hashing
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = create_user(name, mobile, password_hash)
    user_json = UserSchema().dump(user)
    return jsonify({'message': 'Registration successful. Please login.', 'user': user_json}), 201
