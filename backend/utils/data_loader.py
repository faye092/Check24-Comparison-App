import pandas as pd
from datetime import datetime
from ..models import db, Game, StreamingPackage, StreamingOffer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data():
    logger.info("=== Starting Data Load Process ===")
    try:
        # Clear existing data
        StreamingOffer.query.delete()
        StreamingPackage.query.delete()
        Game.query.delete()
        db.session.commit()
        
        # Load Games
        games_df = pd.read_csv("data/bc_game.csv")
        for _, row in games_df.iterrows():
            game = Game(
                id=int(row['id']),
                team_home=row['team_home'],
                team_away=row['team_away'],
                starts_at=datetime.strptime(row['starts_at'], "%Y-%m-%d %H:%M:%S"),
                tournament_name=row['tournament_name']
            )
            db.session.add(game)
        db.session.commit()

        # Load Streaming Packages
        packages_df = pd.read_csv("data/bc_streaming_package.csv")
        for _, row in packages_df.iterrows():
            # Handle NaN values by converting them to 0
            monthly_price = 0 if pd.isna(row['monthly_price_cents']) else int(row['monthly_price_cents'])
            yearly_price = 0 if pd.isna(row['monthly_price_yearly_subscription_in_cents']) else int(row['monthly_price_yearly_subscription_in_cents'])
            
            package = StreamingPackage(
                id=int(row['id']),
                name=row['name'],
                monthly_price_cents=monthly_price,
                monthly_price_yearly_subscription_in_cents=yearly_price
            )
            db.session.add(package)
        db.session.commit()

        # Load Streaming Offers
        offers_df = pd.read_csv("data/bc_streaming_offer.csv")
        for _, row in offers_df.iterrows():
            offer = StreamingOffer(
                game_id=int(row['game_id']),
                streaming_package_id=int(row['streaming_package_id']),
                live=bool(row['live']),
                highlights=bool(row['highlights'])
            )
            db.session.add(offer)
        
        db.session.commit()
        logger.info("Data load completed successfully.")

    except Exception as e:
        logger.error(f"Error during data loading: {e}")
        db.session.rollback()
        raise
