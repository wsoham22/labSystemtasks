import os
from dotenv import load_dotenv
from flask import Flask,request
from controller.userController import user_bp
from controller.productController import product_bp

app = Flask(__name__)

# Load environment variables
load_dotenv(dotenv_path="config.env")

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)

if __name__ == '__main__':
    app.run(debug=True)
