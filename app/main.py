from flask import Flask
from app.api.employee import employee_bp
from app.api.cart import cart_bp
from flask_cors import CORS
from app.api.auth import auth_bp
from app.api.menu import menu_bp
from app.api.order import order_bp
from app.api.user import user_bp
from app.db.database import init_db
from flask_cors import CORS




app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(employee_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(order_bp)
init_db(app)

# Register blueprints

app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
