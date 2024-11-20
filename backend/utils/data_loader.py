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
            db.session.commit() # commit after loading games
            print("Game data loaded successfully")

            # load the package and offer data
            packages_df = pd.read_csv("data/bc_streaming_package.csv")

            # debugging: print loaded games to ensure correct insertion
            inserted_games = Game.query.all()
            print(f"Inserted games count: {len(inserted_games)}")

            # load streaming package data
            packages_df = pd.read_csv("data/bc_streaming_package.csv")
            packages = [
                StreamingPackage(
                    id=row['id'],
                    name=row['name'],
                    monthly_price_cents=row['monthly_price_cents'] if pd.notna(row['monthly_price_cents']) else None,
                    monthly_price_yearly_subscription_in_cents=row['monthly_price_yearly_subscription_in_cents'] if pd.notna(row['monthly_price_yearly_subscription_in_cents']) else None
                )
                for _, row in packages_df.iterrows()
            ]
            db.session.bulk_save_objects(packages)
            db.session.commit()  # commit after loading packages
            print("Streaming package data loaded successfully.")

            # debugging: Print loaded packages to ensure correct insertion
            inserted_packages = StreamingPackage.query.all()
            print(f"Inserted streaming packages count: {len(inserted_packages)}")

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

            # debugging: ensure the game_id and streaming_package_id exist before insertion
            for offer in offers:
                 game_exists = Game.query.get(offer.game_id) is not None
                 package_exists = StreamingPackage.query.get(offer.streaming_package_id) is not None
                 if not game_exists:
                      print(f"Warning: Game with ID {offer.game_id} does not exist.")

                 if not package_exists:
                      print(f"Warning: Streaming package with ID {offer.streaming_package_id} does not exist.")
            db.session.bulk_save_objects(offers)          
            db.session.commit() # commit after loading offers
            print("Streaming offer data loaded successfully.")

            # debugging: print loaded offers to ensure correct insertion
            inserted_offers = StreamingOffer.query.all()
            print(f"Inserted streaming offers count: {len(inserted_offers)}")

    except Exception as e:
        db.session.rollback() # if an error occurs, rollback the changes
        print(f"Error loading data: {e}")