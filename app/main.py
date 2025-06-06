from flask import Flask
from flask_cors import CORS

from app.api.employee import employee_bp
from app.api.cart import cart_bp
from app.api.auth import auth_bp
from app.api.menu import menu_bp
from app.api.order import order_bp
from app.api.user import user_bp
from app.db.database import init_db
from app.api.profile import profile_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(employee_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(order_bp)
init_db(app)
app.register_blueprint(user_bp)
app.register_blueprint(profile_bp)

if __name__ == "__main__":
    app.run(debug=True)
