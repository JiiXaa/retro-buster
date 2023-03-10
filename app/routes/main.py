from flask import Blueprint, render_template


bp = Blueprint("main", __name__, url_prefix="/")

# The main route, accessible to all users, even if they are not logged in


@bp.route("/")
def index():
    return render_template("index.html")
