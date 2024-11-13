from flask import Flask
from db import init_db,db
from models import Game, StreamingPackage, StreamingOffer
from utils.data_loader import load_data
from routes.games import games_blueprint
from routes.packages import packages_blueprint
from routes.offers import offers_blueprint

app = Flask(__name__)
init_db(app)
with app.app_context():
    db.create_all()
    load_data()

app.register_blueprint(games_blueprint, url_prefix="/games")
app.register_blueprint(packages_blueprint, url_prefix="/packages")
app.register_blueprint(offers_blueprint, url_prefix="/offers")

if __name__ == "__main__":
    app.run(debug=True)