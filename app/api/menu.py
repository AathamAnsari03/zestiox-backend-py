from flask import Blueprint, jsonify, request
import mysql.connector

menu_bp = Blueprint('menu', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ansari@2004",
        database="zestiox"
    )

@menu_bp.route('/menu-items', methods=['GET'])
def get_menu():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all categories in id order (eating order)
    cursor.execute("SELECT id, name FROM menu_categories ORDER BY id ASC")
    categories = cursor.fetchall()

    menu = []
    for category in categories:
        cursor.execute(
            "SELECT id, name, price FROM menu_items WHERE category_id = %s",
            (category["id"],)
        )
        items = cursor.fetchall()
        menu.append({
            "id": category["id"],
            "name": category["name"],
            "items": items
        })

    cursor.close()
    conn.close()
    return jsonify(menu)

@menu_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    menu_item_id = data.get('menu_item_id')
    quantity = data.get('quantity', 1)

    if not user_id or not menu_item_id:
        return jsonify({'error': 'user_id and menu_item_id are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if item already in cart
    cursor.execute(
        "SELECT id, quantity FROM cart_items WHERE user_id = %s AND menu_item_id = %s",
        (user_id, menu_item_id)
    )
    row = cursor.fetchone()
    if row:
        new_quantity = row[1] + quantity
        cursor.execute(
            "UPDATE cart_items SET quantity = %s WHERE id = %s",
            (new_quantity, row[0])
        )
    else:
        cursor.execute(
            "INSERT INTO cart_items (user_id, menu_item_id, quantity) VALUES (%s, %s, %s)",
            (user_id, menu_item_id, quantity)
        )

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Item added to cart'}), 201

@menu_bp.route('/cart/count', methods=['GET'])
def cart_count():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(quantity) FROM cart_items WHERE user_id = %s",
        (user_id,)
    )
    result = cursor.fetchone()
    count = result[0] if result[0] is not None else 0

    cursor.close()
    conn.close()
    return jsonify({'count': count})