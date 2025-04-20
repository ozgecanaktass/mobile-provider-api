from flask import Flask
from app.extensions import db, jwt, swagger
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# database connection 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# jwt secret key
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "secret-key")

# swagger configuration with bearer auth
app.config['SWAGGER'] = {
    "title": "Mobile Provider App",
    "uiversion": 3,
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "security": [{"Bearer": []}]
}

# initialize extensions
db.init_app(app)
jwt.init_app(app)
swagger.init_app(app)

# register route blueprints
from app.routes.usage import usage_bp
from app.routes.auth import auth_bp
from app.routes.calculate_bill import bill_bp
from app.routes.billing import billing_bp

app.register_blueprint(usage_bp, url_prefix="/api/v1/usage")
app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
app.register_blueprint(bill_bp, url_prefix="/api/v1")
app.register_blueprint(billing_bp, url_prefix="/api/v1/pay-bill")

if __name__ == "__main__":
    app.run(debug=True)
