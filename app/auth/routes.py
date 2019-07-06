from app.auth import bp


@bp.route("/main", methods=["GET", "POST"])
def login():
    return "WORKS!"
