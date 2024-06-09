import os
from flask import Flask
from celery import Celery
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
load_dotenv()

# Debugging: Print loaded environment variables
print("Loaded Environment Variables:")
print(f"SECRET_KEY: {os.environ.get('SECRET_KEY')}")
print(f"MAIL_USERNAME: {os.environ.get('MAIL_USERNAME')}")
print(f"MAIL_PASSWORD: {os.environ.get('MAIL_PASSWORD')}")
print(f"REDISCLOUD_URL: {os.environ.get('REDISCLOUD_URL')}")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Configure Celery
app.config['CELERY_BROKER_URL'] = os.environ.get('REDISCLOUD_URL')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDISCLOUD_URL')

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

print("Celery broker URL:", celery.conf.broker_url)
print("Celery result backend:", celery.conf.result_backend)
