import pandas as pd
from models import db, Game, StreamingPackage, StreamingOffer

def load_data():
    try:
        with db.session.begin():
            games_df = pd.read_csv("data/bc_game.csv")
            games = [
                Game(
                    id=row['id'],
                    team_home=row['team_home'],
                    team_away=row['team_away'],
                    starts_at=pd.to_datetime(row['starts_at']),
                    tournament_name=row['tournament_name']
                )
                for _, row in games_df.iterrows()
            ]
            db.session.bulk_save_objects(games)

            packages_df = pd.read_csv("data/streaming_packages.csv")
            packages = [
                StreamingPackage(
                    id=row['id'],
                    name=row['name'],
                    monthly_price_cents=row['monthly_price_cents'],
                    monthly_price_yearly_subscription_in_cents=row['monthly_price_yearly_subscription_in_cents']
                )
                for _, row in packages_df.iterrows()
            ]
            db.session.bulk_save_objects(packages)

            offers_df = pd.read_csv("data/streaming_offers.csv")
            offers = [
                StreamingOffer(
                    id=row['id'],
                    game_id=row['game_id'],
                    streaming_package_id=row['streaming_package_id'],
                    live=row['live'],
                    highlights=row['highlights']
                )
                for _, row in offers_df.iterrows()
            ]
            db.session.bulk_save_objects(offers)

    except Exception as e:
        print(f"Error loading data: {e}")