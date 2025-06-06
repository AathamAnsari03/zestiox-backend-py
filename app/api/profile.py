from flask import Blueprint, jsonify
import mysql.connector


profile_bp = Blueprint('profile', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",                     # Change if your MySQL user is different
        password="MySql@123",         # Change if your MySQL password is set
        database="zestiox"
    )

@profile_bp.route('/users/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, name, mobile FROM users WHERE id = %s", (user_id,)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        # Mask password as per requirements in zestiox.md
        user['password'] = "********"
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404