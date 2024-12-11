from flask import Flask
from flask_migrate import Migrate
from db import init_db, db
from models import Game, StreamingPackage, StreamingOffer
from utils.data_loader import load_data
from routes.games import games_blueprint
from routes.packages import packages_blueprint
from routes.offers import offers_blueprint

import os

app = Flask(__name__)

# configuration Management: Using Environment Variables
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'streaming.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the database
init_db(app)

# initialize Flask-Migrate
migrate = Migrate(app, db)

with app.app_context():
    if not os.path.exists(os.path.dirname(DATABASE_PATH)):
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    db.create_all()

    if not Game.query.first():  # check if the database is empty
        load_data()

# register blueprint
app.register_blueprint(games_blueprint, url_prefix="/games")
app.register_blueprint(packages_blueprint, url_prefix="/packages")
app.register_blueprint(offers_blueprint, url_prefix="/offers")

# add a default root route
@app.route("/")
def home():
    return "Welcome to the Check24 Streaming Package Comparison!"

# add custom command to load data
# @app.cli.command("load-data")
# def load_data_command():
#     """Load data into the database."""
#     load_data()

if __name__ == "__main__":
    app.run(debug=True)