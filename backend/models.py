from db import db
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    team_home = db.Column(db.String(100), nullable=False, index=True)
    team_away = db.Column(db.String(100), nullable=False, index=True)
    starts_at = db.Column(DateTime, nullable=False)
    tournament_name = db.Column(db.String(100), nullable=False, index=True)

    offers = db.relationship('StreamingOffer', back_populates='game', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Game(id={self.id}, team_home='{self.team_home}', team_away='{self.team_away}', starts_at='{self.starts_at}', tournament_name='{self.tournament_name}')>"


class StreamingPackage(db.Model):
    __tablename__ = "streaming_packages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    monthly_price_cents = db.Column(db.Integer, nullable=True)
    monthly_price_yearly_subscription_in_cents = db.Column(db.Integer, nullable=False)

    offers = db.relationship('StreamingOffer', back_populates='package', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<StreamingPackage(id={self.id}, name='{self.name}', monthly_price_cents={self.monthly_price_cents}, monthly_price_yearly_subscription_in_cents={self.monthly_price_yearly_subscription_in_cents})>"

class StreamingOffer(db.Model):
    __tablename__ = "streaming_offers"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id", ondelete='CASCADE'), nullable=False)
    streaming_package_id = db.Column(db.Integer, db.ForeignKey("streaming_packages.id", ondelete='CASCADE'), nullable=False)
    live = db.Column(db.Boolean, nullable=False)
    highlights = db.Column(db.Boolean, nullable=False)

    game = db.relationship('Game', back_populates='offers')  
    package = db.relationship('StreamingPackage', back_populates='offers')  

    def __repr__(self):
        return f"<StreamingOffer(id={self.id}, game_id={self.game_id}, streaming_package_id={self.streaming_package_id}, live={self.live}, highlights={self.highlights})>"