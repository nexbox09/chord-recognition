# app.py
from flask import Flask
from web.routes import configure_routes
import os

app = Flask(__name__, template_folder='web/templates')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB limit

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

configure_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)