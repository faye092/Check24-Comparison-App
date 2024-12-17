from ..models import SearchRecord, db, StreamingPackage

def save_search_service(data):

    user_id = data.get("user_id")
    search_params = data.get("search_params")

    if not user_id or not search_params:
        raise ValueError("User ID and search parameters are required")

    record = SearchRecord(user_id=user_id, search_params=search_params)
    db.session.add(record)
    db.session.commit()

def recommend_packages_service(user_id):

    records = SearchRecord.query.filter_by(user_id=user_id).order_by(SearchRecord.created_at.desc()).limit(5).all()

    if not records:
        return []

    # 
    recommended_packages = []
    for record in records:
        params = record.search_params

        # 
        team_name = params.get("team_name")
        if team_name:
            packages = StreamingPackage.query.filter(
                StreamingPackage.name.ilike(f"%{team_name}%")
            ).all()
            recommended_packages.extend([{
                "id": package.id,
                "name": package.name,
                "monthly_price_cents": package.monthly_price_cents,
                "yearly_price_cents": package.monthly_price_yearly_subscription_in_cents
            } for package in packages])

    # 
    seen = set()
    unique_packages = [p for p in recommended_packages if p["id"] not in seen and not seen.add(p["id"])]
    return unique_packages