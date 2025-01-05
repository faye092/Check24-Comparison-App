from ..models import Game
from sqlalchemy import func, or_
from datetime import datetime

def query_games(query, page, per_page):
    games = query.paginate(page=page, per_page=per_page, error_out=False)
    return [
        {
            'id': game.id,
            'team_home': game.team_home,
            'team_away': game.team_away,
            'starts_at': game.starts_at.isoformat(),
            'tournament_name': game.tournament_name,
        }
        for game in games.items
    ]


def get_all_games_service(page, per_page):
    query = Game.query
    return query_games(query, page, per_page)


def get_games_by_team_and_tournament_service(team_names, tournament_names, team_type, page, per_page):
    query = Game.query

    # 处理球队和联赛的筛选
    team_names_lower = [name.lower() for name in team_names if name.strip()]
    tournament_names_lower = [name.lower() for name in tournament_names if name.strip()]

    if team_names and tournament_names:
        # 球队 OR 联赛
        if team_type == 'home':
            query = query.filter(
                or_(
                    func.lower(Game.team_home).in_(team_names_lower),
                    func.lower(Game.tournament_name).in_(tournament_names_lower)
                )
            )
        elif team_type == 'away':
            query = query.filter(
                or_(
                    func.lower(Game.team_away).in_(team_names_lower),
                    func.lower(Game.tournament_name).in_(tournament_names_lower)
                )
            )
        else:  # both
            query = query.filter(
                or_(
                    func.lower(Game.team_home).in_(team_names_lower),
                    func.lower(Game.team_away).in_(team_names_lower),
                    func.lower(Game.tournament_name).in_(tournament_names_lower)
                )
            )
    elif team_names:
        # 仅球队
        if team_type == 'home':
            query = query.filter(func.lower(Game.team_home).in_(team_names_lower))
        elif team_type == 'away':
            query = query.filter(func.lower(Game.team_away).in_(team_names_lower))
        else:  # both
            query = query.filter(
                or_(
                    func.lower(Game.team_home).in_(team_names_lower),
                    func.lower(Game.team_away).in_(team_names_lower)
                )
            )
    elif tournament_names:
        # 仅联赛
        query = query.filter(func.lower(Game.tournament_name).in_(tournament_names_lower))

    return query_games(query, page, per_page)


def get_games_by_team_service(team_names, team_type, page, per_page):
    team_names_lower = [name.lower() for name in team_names if name.strip()]
    query = Game.query

    if not team_names_lower:
        raise ValueError("Team names must be provided.")


    if team_type == "home":
        query = query.filter(func.lower(Game.team_home).in_(team_names_lower))
    elif team_type == "away":
        query = query.filter(func.lower(Game.team_away).in_(team_names_lower))
    else:  # both
        query = query.filter(
            or_(
                func.lower(Game.team_home).in_(team_names_lower),
                func.lower(Game.team_away).in_(team_names_lower)
            )
        )

    return query_games(query, page, per_page)


def get_games_by_tournament_service(tournament_names, page, per_page):
    tournament_names_lower = [name.lower() for name in tournament_names if name.strip()]
    query = Game.query.filter(func.lower(Game.tournament_name).in_(tournament_names_lower))
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
            func.date(Game.starts_at) <= end_date_obj,
        )
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    return query_games(query, page, per_page)
