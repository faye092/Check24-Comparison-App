import pandas as pd
from datetime import datetime
from ..models import db, Game, StreamingPackage, StreamingOffer
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data_in_batches(session, data, model, batch_size=500):
    for i in range(0, len(data), batch_size):
        batch = data[i: i + batch_size]
        session.bulk_save_objects(batch)
        session.commit()

def load_data():
    logger.info("=== Starting Data Load Process ===")
    try:
        # 清理现有数据
        StreamingOffer.query.delete()
        StreamingPackage.query.delete()
        Game.query.delete()
        db.session.commit()
        
        # 加载 Game 数据
        games_df = pd.read_csv("data/bc_game.csv")
        games = []
        for _, row in games_df.iterrows():
            starts_at = datetime.strptime(row['starts_at'], "%Y-%m-%d %H:%M:%S")
            games.append(Game(
                id=row['id'],
                team_home=row['team_home'],
                team_away=row['team_away'],
                starts_at=starts_at,
                tournament_name=row['tournament_name']
            ))
        load_data_in_batches(db.session, games, Game)

        # 加载 StreamingPackage 数据
        packages_df = pd.read_csv("data/bc_streaming_package.csv")
        packages = [
            StreamingPackage(
                id=row['id'],
                name=row['name'],
                monthly_price_cents=row['monthly_price_cents'] or 0,
                monthly_price_yearly_subscription_in_cents=row['monthly_price_yearly_subscription_in_cents'] or 0
            )
            for _, row in packages_df.iterrows()
        ]
        load_data_in_batches(db.session, packages, StreamingPackage)

        # 加载 StreamingOffer 数据
        offers_df = pd.read_csv("data/bc_streaming_offer.csv")
        valid_offers = [
            StreamingOffer(
                game_id=row['game_id'],
                streaming_package_id=row['streaming_package_id'],
                live=bool(row['live']),
                highlights=bool(row['highlights'])
            )
            for _, row in offers_df.iterrows()
        ]
        load_data_in_batches(db.session, valid_offers, StreamingOffer)

        logger.info("Data load completed successfully.")
    except Exception as e:
        logger.error(f"Error during data loading: {e}")
        db.session.rollback()
