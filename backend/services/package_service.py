from ..models import StreamingPackage, StreamingOffer, Game
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from datetime import datetime

# 获取所有套餐服务（分页）
def get_all_packages_service(page, per_page):

    packages = StreamingPackage.query.paginate(page=page, per_page=per_page, error_out=False)
    return [
        {
            "id": package.id,
            "name": package.name,
            "monthly_price_cents": package.monthly_price_cents,
            "yearly_price_cents": package.monthly_price_yearly_subscription_in_cents,
        }
        for package in packages.items
    ]


# 搜索流媒体套餐
def search_packages_service(name, subscription_type):
    """
    根据套餐名称和订阅类型搜索流媒体套餐。
    subscription_type 可选值: 'free', 'yearly_only', 'full'
    """
    query = StreamingPackage.query

    if name:
        query = query.filter(StreamingPackage.name.ilike(f"%{name}%"))

    if subscription_type == "free":
        query = query.filter(
            (StreamingPackage.monthly_price_cents == 0) |
            (StreamingPackage.monthly_price_yearly_subscription_in_cents == 0)
        )
    elif subscription_type == "yearly_only":
        query = query.filter(
            (StreamingPackage.monthly_price_cents.is_(None)) &
            (StreamingPackage.monthly_price_yearly_subscription_in_cents > 0)
        )
    elif subscription_type == "full":
        query = query.filter(
            (StreamingPackage.monthly_price_cents > 0) &
            (StreamingPackage.monthly_price_yearly_subscription_in_cents > 0)
        )

    packages = query.all()
    return [
        {
            "id": package.id,
            "name": package.name,
            "monthly_price_cents": package.monthly_price_cents,
            "monthly_price_yearly_price_cents": package.monthly_price_yearly_subscription_in_cents
        }
        for package in packages
    ]


# 获取相关比赛的 game_id 列表
def get_game_ids_by_filters(tournament_name=None, team_name=None, date=None):
    query = Game.query
    if tournament_name:
        query = query.filter(func.lower(Game.tournament_name).ilike(f"%{tournament_name.lower()}%"))
    if team_name:
        query = query.filter(
            (func.lower(Game.team_home).ilike(f"%{team_name.lower()}%")) |
            (func.lower(Game.team_away).ilike(f"%{team_name.lower()}%"))
        )
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(func.date(Game.starts_at) == date_obj)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    games = query.all()
    return [game.id for game in games]


# 获取套餐与比赛的可用性
def get_package_availability(game_ids):
    offers = (
        StreamingOffer.query.options(joinedload(StreamingOffer.package))
        .filter(StreamingOffer.game_id.in_(game_ids))
        .all()
    )

    # 结构化返回结果
    package_availability = {}
    for offer in offers:
        package_id = offer.streaming_package_id
        if package_id not in package_availability:
            package_availability[package_id] = {
                "id": package_id,
                "name": offer.package.name,
                "monthly_price_cents": offer.package.monthly_price_cents,
                "yearly_price_cents": offer.package.monthly_price_yearly_subscription_in_cents,
                "live": False,
                "highlights": False,
                "covered_games": set(),
            }

        # 更新直播和回放状态
        package_availability[package_id]["live"] |= offer.live
        package_availability[package_id]["highlights"] |= offer.highlights
        package_availability[package_id]["covered_games"].add(offer.game_id)

    return package_availability


# 查找覆盖最多比赛且成本最低的套餐组合
def find_optimal_packages_service(game_ids):
    package_availability = get_package_availability(game_ids)
    remaining_games = set(game_ids)
    optimal_packages = []
    total_cost = 0

    # 贪心算法：选择覆盖最多比赛、成本最低的套餐
    while remaining_games:
        best_package = None
        best_value = 0  

        for package_id, details in package_availability.items():
            covered_games = remaining_games & details["covered_games"]
            price = details["monthly_price_cents"] or details["yearly_price_cents"]
            if price and len(covered_games) > 0:
                value = len(covered_games) / price
                if value > best_value:
                    best_package = package_id
                    best_value = value

        if not best_package:
            break  # 无法覆盖剩余比赛

        # 添加最佳套餐
        selected_package = package_availability[best_package]
        optimal_packages.append(
            {
                "name": selected_package["name"],
                "monthly_price_cents": selected_package["monthly_price_cents"],
                "yearly_price_cents": selected_package["yearly_price_cents"],
                "live": selected_package["live"],
                "highlights": selected_package["highlights"],
                "covered_games": list(selected_package["covered_games"]),
            }
        )
        total_cost += selected_package["monthly_price_cents"] or selected_package["yearly_price_cents"]
        remaining_games -= selected_package["covered_games"]

    return {"packages": optimal_packages, "total_cost": total_cost}


# 综合入口：用户通过输入筛选比赛并获取套餐组合
def get_optimal_packages_by_filters(tournament_name=None, team_name=None, date=None):
    game_ids = get_game_ids_by_filters(tournament_name, team_name, date)
    if not game_ids:
        return {"message": "No matches found for the given filters.", "packages": [], "total_cost": 0}

    return find_optimal_packages_service(game_ids)
