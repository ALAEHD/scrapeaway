import os
from flask import Flask, render_template, request, flash, redirect
from flask_mail import Mail, Message
from scraper import (
    scrape_jumia, scrape_electroplanet, scrape_virgin,
    scrape_marjanemall, scrape_aswakassalam, scrape_mediazone,
    scrape_bestmark, scrape_cosmoselectro, scrape_iris,
    scrape_biougnach, scrape_micromagma, scrape_uno, scrape_ikea,
    scrape_kitea, scrape_bricoma
)
import logging
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Initialize Flask-Mail
mail = Mail(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = os.environ.get('REDISCLOUD_URL')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDISCLOUD_URL')

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Mapping between checkbox values and scraper functions
SCRAPER_MAP = {
    "jumia": scrape_jumia,
    "electroplanet": scrape_electroplanet,
    "virgin": scrape_virgin,
    "marjanemall": scrape_marjanemall,
    "aswakassalam": scrape_aswakassalam,
    "mediazone": scrape_mediazone,
    "bestmark": scrape_bestmark,
    "cosmoselectro": scrape_cosmoselectro,
    "iris": scrape_iris,
    "biougnach": scrape_biougnach,
    "micromagma": scrape_micromagma,
    "uno": scrape_uno,
    "ikea": scrape_ikea,
    "kitea": scrape_kitea,
    "bricoma": scrape_bricoma
}


# Sample route using Celery tasks
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        selected_scrapers = request.form.getlist("scrapers")  # Get list of selected scrapers
        task_results = []
        for scraper_name in selected_scrapers:
            try:
                scraper_func = SCRAPER_MAP.get(scraper_name)
                if scraper_func:
                    # Instead of calling the function directly, delay it as a Celery task
                    task = scraper_func.delay(query)
                    task_results.append(task)
            except Exception as e:
                logger.error(f"Error scraping with {scraper_name}: {e}")

        # Collect results from tasks
        results = []
        for task in task_results:
            try:
                results.extend(task.get(timeout=60))  # Adjust timeout as needed
            except Exception as e:
                logger.error(f"Error getting result from task: {e}")

        return render_template("results.html", query=query, results=results)
    return render_template("index.html")


@app.route('/websites')
def websites():
    return render_template('websites.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = Message(subject='New Contact Form Submission',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']],
                  body=f"Name: {name}\nEmail: {email}\nMessage: {message}")

    mail.send(msg)
    flash('Email sent successfully!', 'success')
    return redirect('/')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)