from flask import Flask, render_template, request, flash, redirect
from scraper import (
    scrape_jumia, scrape_electroplanet, scrape_virgin,
    scrape_marjanemall, scrape_aswakassalam, scrape_mediazone,
    scrape_bestmark, scrape_cosmoselectro, scrape_iris,
    scrape_biougnach, scrape_micromagma, scrape_uno, scrape_ikea,
    scrape_kitea, scrape_bricoma
)
import logging
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'elkandoussialae@gmail.com'
app.config['MAIL_PASSWORD'] = 'dzmu owkr rxjt ugec'

mail = Mail(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        selected_scrapers = request.form.getlist("scrapers")  # Get list of selected scrapers
        results = []
        for scraper_name in selected_scrapers:
            try:
                scraper_func = SCRAPER_MAP.get(scraper_name)
                if scraper_func:
                    results.extend(scraper_func(query))
            except Exception as e:
                logger.error(f"Error scraping with {scraper_name}: {e}")
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
                  recipients=['elkandoussialae@gmail.com'],
                  body=f"Name: {name}\nEmail: {email}\nMessage: {message}")

    mail.send(msg)
    flash('Email sent successfully!', 'success')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
