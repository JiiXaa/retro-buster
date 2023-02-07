from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Videocassette
from app import db

bp = Blueprint("videocassettes", __name__, url_prefix="/videocassettes")

# Utility function to search for vhs tapes by title, director, or genre.
# Returns a list of vhs tapes that match the search criteria (case insensitive)
def search_vhs(search_queries):
    if not search_queries:
        flash("Please provide at least one search term.")

    query = Videocassette.query
    for term in search_queries:
        if term == "title":
            query = query.filter(
                Videocassette.title.ilike("%" + search_queries[term] + "%")
            )
        elif term == "director":
            query = query.filter(
                Videocassette.director.ilike("%" + search_queries[term] + "%")
            )
        elif term == "genre":
            query = query.filter(
                Videocassette.genre.ilike("%" + search_queries[term] + "%")
            )
    return query.all()


@bp.route("/", methods=["GET", "POST"])
def index():
    search_queries = {}
    if request.method == "POST":
        title = request.form.get("title")
        director = request.form.get("director")
        genre = request.form.get("genre")

        if title:
            search_queries["title"] = title
        if director:
            search_queries["director"] = director
        if genre:
            search_queries["genre"] = genre

        vhs_query = search_vhs(search_queries)
        print("vhs_query: ", vhs_query)
        return render_template("videocassettes/vhs_search.html", vhs_query=vhs_query)
    vhs_all = Videocassette.query.all()
    print("vhs_all", vhs_all)
    return render_template("videocassettes/index.html", vhs_all=vhs_all)


@bp.route("/vhs_add", methods=["GET", "POST"])
def vhs_add():
    if request.method == "POST":
        title = request.form.get("title")
        director = request.form.get("director")
        genre = request.form.get("genre")
        vhs = Videocassette(
            title=title,
            director=director,
            genre=genre,
        )
        db.session.add(vhs)
        db.session.commit()
        return redirect(url_for("videocassettes.index"))
    return render_template("videocassettes/vhs_add.html")


@bp.route("/<int:id>/vhs_edit", methods=["GET", "POST"])
def vhs_edit(id):
    vhs = Videocassette.query.get(id)
    if request.method == "POST":
        vhs.title = request.form.get("title")
        vhs.director = request.form.get("director")
        vhs.genre = request.form.get("genre")
        db.session.commit()
        return redirect(url_for("videocassettes.index"))
    return render_template("videocassettes/vhs_edit.html", vhs=vhs)


@bp.route("/<int:id>/delete", methods=["GET", "POST"])
def vhs_delete(id):
    vhs = Videocassette.query.get(id)
    if request.method == "POST":
        db.session.delete(vhs)
        db.session.commit()
        return redirect(url_for("videocassettes.index"))
    return render_template("videocassettes/vhs_delete.html", vhs=vhs)
