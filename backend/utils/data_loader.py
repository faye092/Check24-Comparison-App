import pandas as pd
import logging
from models import db, Game, StreamingPackage, StreamingOffer
from sqlalchemy.orm import load_only

# Configuring logging
logging.basicConfig(filename='data_loader.log', level=logging.WARNING, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    try:
        # Clear existing data
        db.session.query(StreamingOffer).delete()
        db.session.query(Game).delete()
        db.session.query(StreamingPackage).delete()
        db.session.commit()
        
        # Load the game data
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
        db.session.commit()
        print("Game data loaded successfully")

        # Load streaming package data
        packages_df = pd.read_csv("data/bc_streaming_package.csv")
        packages = [
            StreamingPackage(
                id=row['id'],
                name=row['name'],
                monthly_price_cents=row['monthly_price_cents'] if pd.notna(row['monthly_price_cents']) else None,
                monthly_price_yearly_subscription_in_cents=row['monthly_price_yearly_subscription_in_cents']
            )
            for _, row in packages_df.iterrows()
        ]
        db.session.bulk_save_objects(packages)
        db.session.commit()
        print("Streaming package data loaded successfully.")

        # Load the streaming offer data
        offers_df = pd.read_csv("data/bc_streaming_offer.csv")
        offers = []

        # Pre-fetch all existing games and packages to improve performance
        existing_games = set(g.id for g in Game.query.options(load_only(Game.id)).all())
        existing_packages = set(p.id for p in StreamingPackage.query.options(load_only(StreamingPackage.id)).all())

        for _, row in offers_df.iterrows():
            if row['game_id'] in existing_games and row['streaming_package_id'] in existing_packages:
                offers.append(
                    StreamingOffer(
                        game_id=row['game_id'],
                        streaming_package_id=row['streaming_package_id'],
                        live=bool(row['live']),
                        highlights=bool(row['highlights'])
                    )
                )
            else:
                if row['game_id'] not in existing_games:
                    msg = f"Warning: Game with ID {row['game_id']} does not exist."
                    logging.warning(msg)
                    print(msg)
                if row['streaming_package_id'] not in existing_packages:
                    msg = f"Warning: Streaming package with ID {row['streaming_package_id']} does not exist."
                    logging.warning(msg)
                    print(msg)

        if offers:
            db.session.bulk_save_objects(offers)
            db.session.commit()
            print("Streaming offer data loaded successfully.")
        else:
            print("No valid offers to load.")

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error loading data: {e}")
        print(f"Error loading data: {e}")

