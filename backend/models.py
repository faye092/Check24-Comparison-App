from db import db

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    team_home = db.Column(db.String, nullable=False)
    team_away = db.Column(db.String, nullable=False)
    starts_at = db.Column(db.String, nullable=False)
    tournament_name = db.Column(db.String, nullable=False)

class StreamingPackage(db.Model):
    __tablename__ = "streaming_packages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    monthly_price_cents = db.Column(db.Integer, nullable=False)
    monthly_price_yearly_subscription_in_cents = db.Column(db.Integer, nullable=False)

class StreamingOffer(db.Model):
    __tablename__ = "streaming_offers"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    streaming_package_id = db.Column(db.Integer, db.ForeignKey("streaming_packages.id"), nullable=False)
    live = db.Column(db.Boolean, nullable=False)
    highlights = db.Column(db.Boolean, nullable=False)