from flask import Flask
from app.api.employee import employee_bp
from app.api.menu import menu_bp  # Now importing from api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # <-- Add this line

# Register blueprints
app.register_blueprint(employee_bp)
app.register_blueprint(menu_bp)

if __name__ == "__main__":
    app.run(debug=True)