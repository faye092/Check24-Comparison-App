from .games import games_blueprint
from .packages import packages_blueprint
from .searches import searches_blueprint

def register_routes(app):
    app.register_blueprint(games_blueprint, url_prefix="/games")
    app.register_blueprint(packages_blueprint, url_prefix="/packages")
    app.register_blueprint(searches_blueprint, url_prefix="/searches")
