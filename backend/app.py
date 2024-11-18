from flask import Flask
from db import init_db, db
from models import Game, StreamingPackage, StreamingOffer
from utils.data_loader import load_data
from routes.games import games_blueprint
from routes.packages import packages_blueprint
from routes.offers import offers_blueprint

import os

app = Flask(__name__)

# configuration Management: Using Environment Variables
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/streaming.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the database
init_db(app)
with app.app_context():
    db.create_all()
    if not Game.query.first():  # check if the database is empty
        load_data()

# register blueprint
app.register_blueprint(games_blueprint, url_prefix="/games")
app.register_blueprint(packages_blueprint, url_prefix="/packages")
app.register_blueprint(offers_blueprint, url_prefix="/offers")

if __name__ == "__main__":
    app.run(debug=True)