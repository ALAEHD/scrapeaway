# import os
# from flask import Flask, render_template, request, flash, redirect
# from flask_mail import Mail, Message
# from scraper import (
#     scrape_jumia, scrape_electroplanet, scrape_virgin,
#     scrape_marjanemall, scrape_aswakassalam, scrape_mediazone,
#     scrape_bestmark, scrape_cosmoselectro, scrape_iris,
#     scrape_biougnach, scrape_micromagma, scrape_uno, scrape_ikea,
#     scrape_kitea, scrape_bricoma
# )
# import logging
# from celery import Celery
#
# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = '1bec38ee8a3743f74d3b76227b90d65e'
#
# # Configure Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'elkandoussialae@gmail.com'
# app.config['MAIL_PASSWORD'] = 'dzmu owkr rxjt ugec'
#
# # Initialize Flask-Mail
# mail = Mail(app)
#
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Initialize Celery
# celery = Celery(__name__)
#
# # Mapping between checkbox values and scraper functions
# SCRAPER_MAP = {
#     "jumia": scrape_jumia,
#     "electroplanet": scrape_electroplanet,
#     "virgin": scrape_virgin,
#     "marjanemall": scrape_marjanemall,
#     "aswakassalam": scrape_aswakassalam,
#     "mediazone": scrape_mediazone,
#     "bestmark": scrape_bestmark,
#     "cosmoselectro": scrape_cosmoselectro,
#     "iris": scrape_iris,
#     "biougnach": scrape_biougnach,
#     "micromagma": scrape_micromagma,
#     "uno": scrape_uno,
#     "ikea": scrape_ikea,
#     "kitea": scrape_kitea,
#     "bricoma": scrape_bricoma
# }
#
# # Sample route using Celery tasks
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         query = request.form["query"]
#         selected_scrapers = request.form.getlist("scrapers")  # Get list of selected scrapers
#         results = []
#         for scraper_name in selected_scrapers:
#             try:
#                 scraper_func = SCRAPER_MAP.get(scraper_name)
#                 if scraper_func:
#                     # Instead of calling the function directly, delay it as a Celery task
#                     result = scraper_func.delay(query)
#                     results.extend(result.get())  # Get the result from the Celery task
#             except Exception as e:
#                 logger.error(f"Error scraping with {scraper_name}: {e}")
#         return render_template("results.html", query=query, results=results)
#     return render_template("index.html")
#
# @app.route('/websites')
# def websites():
#     return render_template('websites.html')
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
# @app.route('/contacts')
# def contacts():
#     return render_template('contacts.html')
#
# @app.route('/results')
# def results():
#     return render_template('results.html')
#
# @app.route('/send_email', methods=['POST'])
# def send_email():
#     name = request.form['name']
#     email = request.form['email']
#     message = request.form['message']
#
#     msg = Message(subject='New Contact Form Submission',
#                   sender=app.config['MAIL_USERNAME'],
#                   recipients=['elkandoussialae@gmail.com'],
#                   body=f"Name: {name}\nEmail: {email}\nMessage: {message}")
#
#     mail.send(msg)
#     flash('Email sent successfully!', 'success')
#     return redirect('/')
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)



# import os
# from flask import Flask, render_template, request, flash, redirect
# from flask_mail import Mail, Message
# from scraper import (
#     scrape_jumia, scrape_electroplanet, scrape_virgin,
#     scrape_marjanemall, scrape_aswakassalam, scrape_mediazone,
#     scrape_bestmark, scrape_cosmoselectro, scrape_iris,
#     scrape_biougnach, scrape_micromagma, scrape_uno, scrape_ikea,
#     scrape_kitea, scrape_bricoma
# )
# import logging
# from celery import Celery
#
# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET_KEY', '1bec38ee8a3743f74d3b76227b90d65e')  # Use an environment variable
#
# # Configure Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'elkandoussialae@gmail.com')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'dzmu owkr rxjt ugec')
#
# # Initialize Flask-Mail
# mail = Mail(app)
#
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Configure Celery
# app.config['CELERY_BROKER_URL'] = os.environ.get('REDISCLOUD_URL', os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))
# app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDISCLOUD_URL', os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))
#
# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#
#     class ContextTask(TaskBase):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery
#
# celery = make_celery(app)
#
# # Mapping between checkbox values and scraper functions
# SCRAPER_MAP = {
#     "jumia": scrape_jumia,
#     "electroplanet": scrape_electroplanet,
#     "virgin": scrape_virgin,
#     "marjanemall": scrape_marjanemall,
#     "aswakassalam": scrape_aswakassalam,
#     "mediazone": scrape_mediazone,
#     "bestmark": scrape_bestmark,
#     "cosmoselectro": scrape_cosmoselectro,
#     "iris": scrape_iris,
#     "biougnach": scrape_biougnach,
#     "micromagma": scrape_micromagma,
#     "uno": scrape_uno,
#     "ikea": scrape_ikea,
#     "kitea": scrape_kitea,
#     "bricoma": scrape_bricoma
# }
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         query = request.form["query"]
#         selected_scrapers = request.form.getlist("scrapers")  # Get list of selected scrapers
#         task = scrape_products_task.apply_async(args=[query, selected_scrapers])
#         return redirect(f'/status/{task.id}')
#     return render_template("index.html")
#
# @app.route('/websites')
# def websites():
#     return render_template('websites.html')
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
# @app.route('/contacts')
# def contacts():
#     return render_template('contacts.html')
#
# @app.route('/results')
# def results():
#     return render_template('results.html')
#
# @app.route('/send_email', methods=['POST'])
# def send_email():
#     name = request.form['name']
#     email = request.form['email']
#     message = request.form['message']
#
#     msg = Message(subject='New Contact Form Submission',
#                   sender=app.config['MAIL_USERNAME'],
#                   recipients=['elkandoussialae@gmail.com'],
#                   body=f"Name: {name}\nEmail: {email}\nMessage: {message}")
#
#     mail.send(msg)
#     flash('Email sent successfully!', 'success')
#     return redirect('/')
#
# @app.route('/status/<task_id>')
# def task_status(task_id):
#     task = scrape_products_task.AsyncResult(task_id)
#     if task.state == 'PENDING':
#         response = {
#             'state': task.state,
#             'status': 'Pending...'
#         }
#     elif task.state != 'FAILURE':
#         response = {
#             'state': task.state,
#             'status': task.info.get('status', '')
#         }
#         if 'results' in task.info:
#             response['results'] = task.info['results']
#     else:
#         response = {
#             'state': task.state,
#             'status': str(task.info)
#         }
#     return render_template('status.html', response=response)
#
# @celery.task(bind=True)
# def scrape_products_task(self, query, selected_scrapers):
#     self.update_state(state='PROGRESS', meta={'status': 'Scraping in progress...'})
#     results = []
#     for scraper_name in selected_scrapers:
#         try:
#             scraper_func = SCRAPER_MAP.get(scraper_name)
#             if scraper_func:
#                 results.extend(scraper_func(query))
#         except Exception as e:
#             logger.error(f"Error scraping with {scraper_name}: {e}")
#     return {'status': 'Task completed!', 'results': results}
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)



# import os
# from flask import Flask, render_template, request, flash, redirect
# from flask_mail import Mail, Message
# from scraper import (
#     scrape_jumia, scrape_electroplanet, scrape_virgin,
#     scrape_marjanemall, scrape_aswakassalam, scrape_mediazone,
#     scrape_bestmark, scrape_cosmoselectro, scrape_iris,
#     scrape_biougnach, scrape_micromagma, scrape_uno, scrape_ikea,
#     scrape_kitea, scrape_bricoma
# )
# import logging
# from celery import Celery
#
# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET_KEY', '1bec38ee8a3743f74d3b76227b90d65e')  # Use an environment variable
#
# # Configure Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'elkandoussialae@gmail.com'
# app.config['MAIL_PASSWORD'] = 'dzmu owkr rxjt ugec'
#
# # Initialize Flask-Mail
# mail = Mail(app)
#
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Configure Celery
# app.config['CELERY_BROKER_URL'] = os.environ.get('REDISCLOUD_URL')
# app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDISCLOUD_URL')
#
# # Initialize Celery
# celery = Celery(__name__)
#
# # Mapping between checkbox values and scraper functions
# SCRAPER_MAP = {
#     "jumia": scrape_jumia,
#     "electroplanet": scrape_electroplanet,
#     "virgin": scrape_virgin,
#     "marjanemall": scrape_marjanemall,
#     "aswakassalam": scrape_aswakassalam,
#     "mediazone": scrape_mediazone,
#     "bestmark": scrape_bestmark,
#     "cosmoselectro": scrape_cosmoselectro,
#     "iris": scrape_iris,
#     "biougnach": scrape_biougnach,
#     "micromagma": scrape_micromagma,
#     "uno": scrape_uno,
#     "ikea": scrape_ikea,
#     "kitea": scrape_kitea,
#     "bricoma": scrape_bricoma
# }
#
# # Sample route using Celery tasks
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         query = request.form["query"]
#         selected_scrapers = request.form.getlist("scrapers")  # Get list of selected scrapers
#         results = []
#         for scraper_name in selected_scrapers:
#             try:
#                 scraper_func = SCRAPER_MAP.get(scraper_name)
#                 if scraper_func:
#                     # Instead of calling the function directly, delay it as a Celery task
#                     result = scraper_func.delay(query)
#                     results.extend(result.get())  # Get the result from the Celery task
#             except Exception as e:
#                 logger.error(f"Error scraping with {scraper_name}: {e}")
#         return render_template("results.html", query=query, results=results)
#     return render_template("index.html")
#
# @app.route('/websites')
# def websites():
#     return render_template('websites.html')
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
# @app.route('/contacts')
# def contacts():
#     return render_template('contacts.html')
#
# @app.route('/results')
# def results():
#     return render_template('results.html')
#
# @app.route('/send_email', methods=['POST'])
# def send_email():
#     name = request.form['name']
#     email = request.form['email']
#     message = request.form['message']
#
#     msg = Message(subject='New Contact Form Submission',
#                   sender=app.config['MAIL_USERNAME'],
#                   recipients=['elkandoussialae@gmail.com'],
#                   body=f"Name: {name}\nEmail: {email}\nMessage: {message}")
#
#     mail.send(msg)
#     flash('Email sent successfully!', 'success')
#     return redirect('/')
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)


# import os
# from flask import Flask, render_template, request, flash, redirect
# from flask_mail import Mail, Message
# from scraper import (
#     scrape_jumia, scrape_electroplanet, scrape_virgin,
#     scrape_marjanemall, scrape_aswakassalam, scrape_mediazone,
#     scrape_bestmark, scrape_cosmoselectro, scrape_iris,
#     scrape_biougnach, scrape_micromagma, scrape_uno, scrape_ikea,
#     scrape_kitea, scrape_bricoma
# )
# import logging
# from celery import Celery
#
# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')
#
# # Configure Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
#
# # Initialize Flask-Mail
# mail = Mail(app)
#
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Configure Celery
# app.config['CELERY_BROKER_URL'] = os.environ.get('REDISCLOUD_URL')
# app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDISCLOUD_URL')
#
# # Initialize Celery
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)
#
# # Mapping between checkbox values and scraper functions
# SCRAPER_MAP = {
#     "jumia": scrape_jumia,
#     "electroplanet": scrape_electroplanet,
#     "virgin": scrape_virgin,
#     "marjanemall": scrape_marjanemall,
#     "aswakassalam": scrape_aswakassalam,
#     "mediazone": scrape_mediazone,
#     "bestmark": scrape_bestmark,
#     "cosmoselectro": scrape_cosmoselectro,
#     "iris": scrape_iris,
#     "biougnach": scrape_biougnach,
#     "micromagma": scrape_micromagma,
#     "uno": scrape_uno,
#     "ikea": scrape_ikea,
#     "kitea": scrape_kitea,
#     "bricoma": scrape_bricoma
# }
#
#
# # Sample route using Celery tasks
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         query = request.form["query"]
#         selected_scrapers = request.form.getlist("scrapers")  # Get list of selected scrapers
#         task_results = []
#         for scraper_name in selected_scrapers:
#             try:
#                 scraper_func = SCRAPER_MAP.get(scraper_name)
#                 if scraper_func:
#                     # Instead of calling the function directly, delay it as a Celery task
#                     task = scraper_func.delay(query)
#                     task_results.append(task)
#             except Exception as e:
#                 logger.error(f"Error scraping with {scraper_name}: {e}")
#
#         # Collect results from tasks
#         results = []
#         for task in task_results:
#             try:
#                 results.extend(task.get(timeout=60))  # Adjust timeout as needed
#             except Exception as e:
#                 logger.error(f"Error getting result from task: {e}")
#
#         return render_template("results.html", query=query, results=results)
#     return render_template("index.html")
#
#
# @app.route('/websites')
# def websites():
#     return render_template('websites.html')
#
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
#
# @app.route('/contacts')
# def contacts():
#     return render_template('contacts.html')
#
#
# @app.route('/results')
# def results():
#     return render_template('results.html')
#
#
# @app.route('/send_email', methods=['POST'])
# def send_email():
#     name = request.form['name']
#     email = request.form['email']
#     message = request.form['message']
#
#     msg = Message(subject='New Contact Form Submission',
#                   sender=app.config['MAIL_USERNAME'],
#                   recipients=['elkandoussialae@gmail.com'],
#                   body=f"Name: {name}\nEmail: {email}\nMessage: {message}")
#
#     mail.send(msg)
#     flash('Email sent successfully!', 'success')
#     return redirect('/')
#
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)

# import os
# from flask import Flask, render_template, request, flash, redirect, Response, stream_with_context
# from flask_mail import Mail, Message
# from scraper import (
#     scrape_jumia, scrape_electroplanet, scrape_virgin,
#     scrape_marjanemall, scrape_aswakassalam, scrape_mediazone,
#     scrape_bestmark, scrape_cosmoselectro, scrape_iris,
#     scrape_biougnach, scrape_micromagma, scrape_uno, scrape_ikea,
#     scrape_kitea, scrape_bricoma
# )
# import logging
# from celery import Celery
#
# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET_KEY', '1bec38ee8a3743f74d3b76227b90d65e')
#
# # Configure Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
#
# # Initialize Flask-Mail
# mail = Mail(app)
#
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Configure Celery
# app.config['CELERY_BROKER_URL'] = os.environ.get('REDISCLOUD_URL')
# app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDISCLOUD_URL')
#
# # Initialize Celery
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)
#
# # Mapping between checkbox values and scraper functions
# SCRAPER_MAP = {
#     "jumia": scrape_jumia,
#     "electroplanet": scrape_electroplanet,
#     "virgin": scrape_virgin,
#     "marjanemall": scrape_marjanemall,
#     "aswakassalam": scrape_aswakassalam,
#     "mediazone": scrape_mediazone,
#     "bestmark": scrape_bestmark,
#     "cosmoselectro": scrape_cosmoselectro,
#     "iris": scrape_iris,
#     "biougnach": scrape_biougnach,
#     "micromagma": scrape_micromagma,
#     "uno": scrape_uno,
#     "ikea": scrape_ikea,
#     "kitea": scrape_kitea,
#     "bricoma": scrape_bricoma
# }
#
# # Sample route using Celery tasks
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         query = request.form["query"]
#         selected_scrapers = request.form.getlist("scrapers")  # Get list of selected scrapers
#         task_results = []
#         for scraper_name in selected_scrapers:
#             try:
#                 scraper_func = SCRAPER_MAP.get(scraper_name)
#                 if scraper_func:
#                     # Instead of calling the function directly, delay it as a Celery task
#                     task = scraper_func.delay(query)
#                     task_results.append(task)
#             except Exception as e:
#                 logger.error(f"Error scraping with {scraper_name}: {e}")
#
#         return Response(stream_with_context(event_stream(task_results, query)))
#     return render_template("index.html")
#
# def event_stream(task_results, query):
#     yield 'data: {}\n\n'.format("Scraping started...")
#     for task in task_results:
#         try:
#             results = task.get(timeout=60)  # Adjust timeout as needed
#             yield 'data: {}\n\n'.format(results)
#         except Exception as e:
#             logger.error(f"Error getting result from task: {e}")
#             yield 'data: {}\n\n'.format(f"Error: {e}")
#     yield 'data: {}\n\n'.format("Scraping finished.")
#
# @app.route('/websites')
# def websites():
#     return render_template('websites.html')
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
# @app.route('/contacts')
# def contacts():
#     return render_template('contacts.html')
#
# @app.route('/results')
# def results():
#     return render_template('results.html')
#
# @app.route('/send_email', methods=['POST'])
# def send_email():
#     name = request.form['name']
#     email = request.form['email']
#     message = request.form['message']
#
#     msg = Message(subject='New Contact Form Submission',
#                   sender=app.config['MAIL_USERNAME'],
#                   recipients=['elkandoussialae@gmail.com'],
#                   body=f"Name: {name}\nEmail: {email}\nMessage: {message}")
#
#     mail.send(msg)
#     flash('Email sent successfully!', 'success')
#     return redirect('/')
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)



import os
from flask import Flask, render_template, request, flash, redirect, Response, jsonify
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

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '1bec38ee8a3743f74d3b76227b90d65e')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
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
        task_ids = []

        for scraper_name in selected_scrapers:
            try:
                scraper_func = SCRAPER_MAP.get(scraper_name)
                if scraper_func:
                    task = scraper_func.delay(query)
                    task_ids.append(task.id)
            except Exception as e:
                logger.error(f"Error scraping with {scraper_name}: {e}")

        # Return task IDs as JSON response
        return jsonify({"task_ids": task_ids})

    return render_template("index.html")

@app.route("/check_task_status", methods=["POST"])
def check_task_status():
    task_ids = request.json.get("task_ids")
    results = {}

    for task_id in task_ids:
        task = celery.AsyncResult(task_id)
        results[task_id] = {"status": task.status}

        if task.successful():
            results[task_id]["result"] = task.get()
        elif task.failed():
            results[task_id]["error"] = str(task.result)

    return jsonify(results)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
