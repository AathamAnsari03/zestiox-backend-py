from flask import Flask
from app.api.employee import employee_bp
from app.api.user import user_bp
from app.db.database import init_db
from flask_cors import CORS




app = Flask(__name__)
CORS(app)
init_db(app)

# Register blueprints
app.register_blueprint(employee_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)