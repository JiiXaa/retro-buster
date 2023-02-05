from flask import Blueprint, render_template, request
from app.models import Videocassette

bp = Blueprint("videocassettes", __name__, url_prefix="/videocassettes")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        director = request.form.get("director")
        genre = request.form.get("genre")

        query = Videocassette.query
        if title:
            query = query.filter(Videocassette.title.like(f"%{title}%"))
        if director:
            query = query.filter(Videocassette.director.like(f"%{director}%"))
        if genre:
            query = query.filter(Videocassette.genre.like(f"%{genre}%"))

        vhs_query = query.all()
        print(vhs_query)
        return render_template(
            "videocassettes/videocassettes_search.html", vhs_query=vhs_query
        )
    all_vhs = Videocassette.query.all()
    print(all_vhs)
    return render_template("videocassettes/index.html", all_vhs=all_vhs)
