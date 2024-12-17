from ..models import Game
from sqlalchemy import func
from datetime import datetime

def query_games(query, page, per_page):
    games = query.paginate(page=page, per_page=per_page, error_out=False)
    return [{
        'id': game.id,
        'team_home': game.team_home,
        'team_away': game.team_away,
        'starts_at': game.starts_at.isoformat(),
        'tournament_name': game.tournament_name
    } for game in games.items]

def get_all_games_service(page, per_page):
    query = Game.query
    return query_games(query, page, per_page)


def get_games_by_team_service(team_name, team_type, page, per_page):
    if team_type == 'home':
        query = Game.query.filter(func.lower(Game.team_home) == team_name.lower())
    elif team_type == 'away':
        query = Game.query.filter(func.lower(Game.team_away) == team_name.lower())
    else:
        query = Game.query.filter(
            (func.lower(Game.team_home) == team_name.lower()) |
            (func.lower(Game.team_away) == team_name.lower())
        )
    return query_games(query, page, per_page)


def get_games_by_tournament_service(tournament_name, page, per_page):
    query = Game.query.filter(
        func.lower(Game.tournament_name).ilike(f'%{tournament_name.lower()}%')
    )
    return query_games(query, page, per_page)


def get_games_by_date_service(date, page, per_page):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        query = Game.query.filter(func.date(Game.starts_at) == date_obj)
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    return query_games(query, page, per_page)

def get_games_by_date_range_service(start_date, end_date, page, per_page):
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        if start_date_obj > end_date_obj:
            raise ValueError("start_date cannot be later than end_date.")
        query = Game.query.filter(
            func.date(Game.starts_at) >= start_date_obj,
            func.date(Game.starts_at) <= end_date_obj
        )
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    return query_games(query, page, per_page)
