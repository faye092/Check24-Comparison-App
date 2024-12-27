from ..models import SearchRecord, Game, StreamingPackage, StreamingOffer
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from ..db import db

def save_search_service(data):

    user_id = data.get("user_id")
    search_params = data.get("search_params")

    if not user_id or not search_params:
        raise ValueError("User ID and search parameters are required")

    search_record = SearchRecord(user_id=user_id, search_params=search_params)
    db.session.add(search_record)
    db.session.commit()

def recommend_packages_service(user_id):

    recent_search = (
        SearchRecord.query.filter_by(user_id=user_id)
        .order_by(SearchRecord.created_at.desc())
        .first()
    )

    if not recent_search:
        return {"message": "No recent searches found for the user.", "recommendations": []}

    # 提取搜索参数
    search_params = recent_search.search_params
    team_name = search_params.get('team_name')
    tournament_name = search_params.get('tournament_name')
    date = search_params.get('date')

    # 根据搜索参数获取相关比赛的 ID
    query = Game.query
    if team_name:
        query = query.filter(
            (func.lower(Game.team_home).ilike(f"%{team_name.lower()}%")) |
            (func.lower(Game.team_away).ilike(f"%{team_name.lower()}%"))
        )
    if tournament_name:
        query = query.filter(func.lower(Game.tournament_name).ilike(f"%{tournament_name.lower()}%"))
    if date:
        try:
            date_obj = func.date(func.date(Game.starts_at)) >= date
            query = query.filter(date_obj)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        
    games = query.all()
    game_ids = [game.id for game in games]

    if not game_ids:
        return {"message": "No matches found for the given filters.", "recommendations": []}
    
    # 获取最佳套餐组合
    offers = (
        StreamingOffer.query.options(joinedload(StreamingOffer.package))
        .filter(StreamingOffer.game_id.in_(game_ids))
        .all()
    )

    # 推荐结果
    package_recommendations = {}
    for offer in offers:
        package = offer.package
        if package.id not in package_recommendations:
            package_recommendations[package.id] = {
                "id": package.id,
                "name": package.name,
                "monthly_price_cents": package.monthly_price_cents,
                "monthly_price_yearly_subscription_in_cents": package.monthly_price_yearly_subscription_in_cents,
                "live_coverage": 0,
                "highlight_coverage": 0,
            }

        if offer.live:
            package_recommendations[package.id]["live_coverage"] += 1
        if offer.highlights:
            package_recommendations[package.id]["highlight_coverage"] += 1

    # 将推荐结果排序（按直播覆盖率和高亮覆盖率降序排列）
    sorted_recommendations = sorted(
        package_recommendations.values(),
        key=lambda x: (x["live_coverage"], x["highlight_coverage"]),
        reverse=True,
    )

    return {"message": "Recommended packages based on your search history", "recommendations": sorted_recommendations}