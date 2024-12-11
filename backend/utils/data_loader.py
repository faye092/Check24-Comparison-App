import pandas as pd
import logging
from models import db, Game, StreamingPackage, StreamingOffer
from sqlalchemy.orm import load_only

# Configuring logging
logging.basicConfig(filename='data_loader.log', level=logging.WARNING, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    try:
        print("\n=== Starting Data Load Process ===")
        
        # 首先清空现有的offers数据
        print("Clearing existing offers data...")
        db.session.query(StreamingOffer).delete()
        db.session.commit()
        
        # 加载和验证CSV数据
        offers_df = pd.read_csv("data/bc_streaming_offer.csv")
        print(f"\nLoaded {len(offers_df)} records from CSV")
        
        # 验证外键关系
        game_ids = set(offers_df['game_id'].unique())
        package_ids = set(offers_df['streaming_package_id'].unique())
        existing_game_ids = set(g.id for g in Game.query.all())
        existing_package_ids = set(p.id for p in StreamingPackage.query.all())
        
        print("\nValidating foreign key relationships:")
        print(f"Games - Required: {len(game_ids)}, Available: {len(existing_game_ids)}")
        print(f"Packages - Required: {len(package_ids)}, Available: {len(existing_package_ids)}")
        
        # 验证数据完整性
        valid_offers = offers_df[
            offers_df['game_id'].isin(existing_game_ids) & 
            offers_df['streaming_package_id'].isin(existing_package_ids)
        ]
        
        print(f"\nValid offers to load: {len(valid_offers)} out of {len(offers_df)}")
        
        # 批量加载数据
        batch_size = 1000
        for i in range(0, len(valid_offers), batch_size):
            batch = valid_offers.iloc[i:i + batch_size]
            offers = [
                StreamingOffer(
                    game_id=row['game_id'],
                    streaming_package_id=row['streaming_package_id'],
                    live=bool(row['live']),
                    highlights=bool(row['highlights'])
                )
                for _, row in batch.iterrows()
            ]
            db.session.bulk_save_objects(offers)
            db.session.commit()
            print(f"Processed {i + len(batch)} offers")
        
        # 验证最终结果
        final_count = StreamingOffer.query.count()
        print(f"\nFinal validation - Loaded offers: {final_count}")
        
    except Exception as e:
        db.session.rollback()
        print(f"\nError during data load: {e}")
        raise
