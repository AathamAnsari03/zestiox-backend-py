from flask import Blueprint, request, jsonify
import mysql.connector

cart_bp = Blueprint('cart', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='MySql@123',
        database='zestiox'
    )

def fetch_cart(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            ci.id,
            mi.name,
            ci.quantity,
            mi.price,
            (ci.quantity * mi.price) AS line_total
        FROM cart_items ci
        JOIN menu_items mi ON ci.menu_item_id = mi.id
        WHERE ci.user_id = %s
    """
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()
    cursor.close()
    conn.close()
    grand_total = sum(item['line_total'] for item in cart_items)
    return cart_items, grand_total

# GET /carts?userId=<id>
@cart_bp.route('/carts', methods=['GET'])
def get_cart():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"error": "userId is required"}), 400
    cart_items, grand_total = fetch_cart(user_id)
    return jsonify({"cart": cart_items, "grand_total": grand_total})

# PUT /carts/<cart_item_id>?userId=<id>
@cart_bp.route('/carts/<int:cart_item_id>', methods=['PUT'])
def update_cart_item(cart_item_id):
    data = request.get_json()
    quantity = data.get('quantity')
    if quantity is None or quantity < 1:
        return jsonify({"error": "Quantity must be at least 1"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cart_items SET quantity = %s WHERE id = %s",
        (quantity, cart_item_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return { "message": "Cart item updated successfully" }

# DELETE /carts/<cart_item_id>?userId=<id>
@cart_bp.route('/carts/<int:cart_item_id>', methods=['DELETE'])
def delete_cart_item(cart_item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cart_items WHERE id = %s",
        (cart_item_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Cart item deleted successfully"}), 200

@cart_bp.route('/orders', methods=['POST'])
def place_order():
    user_id = request.args.get('userId')
    if not user_id:
        data = request.get_json(silent=True)
        user_id = data.get('userId') if data else None
    if not user_id:
        return jsonify({"error": "userId is required"}), 400

    # Fetch cart items for the user
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ci.menu_item_id, ci.quantity, mi.price
        FROM cart_items ci
        JOIN menu_items mi ON ci.menu_item_id = mi.id
        WHERE ci.user_id = %s
    """, (user_id,))
    cart_items = cursor.fetchall()
    if not cart_items:
        cursor.close()
        conn.close()
        return jsonify({"error": "Cart is empty"}), 400

    # Calculate total amount
    total_amount = sum(item['quantity'] * float(item['price']) for item in cart_items)

    # Insert new order
    cursor.execute(
        "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s)",
        (user_id, total_amount, 'Preparing')
    )
    order_id = cursor.lastrowid

    # Insert order items
    for item in cart_items:
        cursor.execute(
            "INSERT INTO order_items (order_id, menu_item_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (order_id, item['menu_item_id'], item['quantity'], item['price'])
        )

    # Clear user's cart
    cursor.execute("DELETE FROM cart_items WHERE user_id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "order placed", "order_id": order_id}), 201