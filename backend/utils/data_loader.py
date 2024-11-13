import pandas as pd
from models import db, Game, StreamingPackage, StreamingOffer

def load_data():
    games_df = pd.read_csv("data/games.csv")
    for _, game in games_df.iterrows():
        game = Game(
            id=row['id'],
            team_home=row['team_home'],
            team_away=row['team_away'],
            starts_at=row['starts_at'],
            tournament_name=row['tournament_name']
        )
        db.session.add(game)
    db.session.commit()

    packages_df = pd.read_csv("data/streaming_packages.csv")
    for _, package in packages_df.iterrows():
        package = StreamingPackage(
            id=row['id'],
            name=row['name'],
            monthly_price_cents=row['monthly_price_cents'],
            monthly_price_yearly_subscription_in_cents=row['monthly_price_yearly_subscription_in_cents']
        )
        db.session.add(package)
    db.session.commit()

    offers_df = pd.read_csv("data/streaming_offers.csv")
    for _, offer in offers_df.iterrows():
        offer = StreamingOffer(
            id=row['id'],
            game_id=row['game_id'],
            streaming_package_id=row['streaming_package_id'],
            live=row['live'],
            highlights=row['highlights']
        )
        db.session.add(offer)
    db.session.commit()