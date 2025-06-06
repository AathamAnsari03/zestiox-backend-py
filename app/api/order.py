from flask import Blueprint, jsonify, request, abort
import mysql.connector

order_bp = Blueprint('order', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',  # Change as needed
        database='zestiox'
    )

@order_bp.route('/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, order_date, total_amount, status
        FROM orders
        WHERE user_id = %s
        ORDER BY order_date DESC
    """, (user_id,))
    orders = cursor.fetchall()
    for order in orders:
        cursor.execute("""
            SELECT oi.menu_item_id, mi.name, oi.quantity, oi.price
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = %s
        """, (order['id'],))
        order['items'] = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(orders)

@order_bp.route('/orders/cancel/<int:order_id>', methods=['PUT', 'POST'])
def cancel_order(order_id): 
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Check if order exists and is not already delivered/cancelled
    cursor.execute("""
        SELECT status FROM orders WHERE id = %s
    """, (order_id,))
    order = cursor.fetchone()
    if not order or order['status'] in ('Delivered', 'Cancelled'):
        cursor.close()
        conn.close()
        abort(400)
    # Update status to Cancelled
    cursor.execute("""
        UPDATE orders SET status = 'Cancelled' WHERE id = %s
    """, (order_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204