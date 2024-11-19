import pandas as pd
from models import db, Game, StreamingPackage, StreamingOffer

def load_data():
    try:
            # load the game data
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

            # load the package and offer data
            packages_df = pd.read_csv("data/bc_streaming_package.csv")

            # process streaming package data
            # if monthly_price_cents is NaN and the annual subscription fee is not 0, it is considered that the monthly subscription service is not provided
            packages_df['monthly_price_cents'] = packages_df['monthly_price_cents'].fillna(-1).astype(int)
            packages_df['monthly_price_yearly_subscription_in_cents'] = packages_df['monthly_price_yearly_subscription_in_cents'].fillna(0).astype(int)

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

            # load the offer data
            offers_df = pd.read_csv("data/bc_streaming_offer.csv")
            offers = [
                StreamingOffer(
                    game_id=row['game_id'],
                    streaming_package_id=row['streaming_package_id'],
                    live=row['live'],
                    highlights=row['highlights']
                )
                for _, row in offers_df.iterrows()
            ]
            db.session.bulk_save_objects(offers)

            # commit the changes
            db.session.commit()

    except Exception as e:
        db.session.rollback() # if an error occurs, rollback the changes
        print(f"Error loading data: {e}")