from flask import Flask
from flask_cors import CORS



from app.api.employee import employee_bp
from app.api.profile import profile_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(employee_bp)
app.register_blueprint(profile_bp)

if __name__ == "__main__":
    app.run(debug=True)