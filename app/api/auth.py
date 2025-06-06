# app/api/auth.py
from flask import Blueprint, request, jsonify
import pymysql
import bcrypt

auth_bp = Blueprint('auth', __name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Senthamil@14',  # <-- change this
        db='zestiox',
        cursorclass=pymysql.cursors.DictCursor
    )

@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    mobile = data.get('mobile')
    password = data.get('password')

    if not mobile or not password:
        return jsonify({'error': 'Mobile and password required'}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE mobile=%s"
            cursor.execute(sql, (mobile,))
            user = cursor.fetchone()
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                return jsonify({'message': 'Authentication successful', 'user': {'id': user['id'], 'name': user['name'], 'mobile': user['mobile']}})
            else:
                return jsonify({'error': 'Invalid mobile or password'}), 401
    finally:
        conn.close()