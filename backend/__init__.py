import os
from flask import Flask
from .db import db
from .models import Game
from .utils.data_loader import load_data
from .routes import register_routes

def create_app():
    app = Flask(__name__)

    # 配置数据库路径
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'streaming.db')

    if not os.path.exists(os.path.dirname(DATABASE_PATH)):
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    db.init_app(app)

    with app.app_context():
        db.create_all()
        if not db.session.query(Game).first():
            print("Loading initial data...")
            load_data()

    
    register_routes(app)

    @app.route("/")
    def home():
        return {
            "message": "Welcome to the Check24 Streaming Package Comparison!",
            "available_routes": [
                "/games",
                "/packages",
                "/searches"
            ]
        }

    return app
