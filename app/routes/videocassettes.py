from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Videocassette, Details
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
        # Basic vhs data
        title = request.form.get("title")
        director = request.form.get("director")
        genre = request.form.get("genre")

        # Additional vhs data stored in the details table
        stock = request.form.get("stock")
        length = request.form.get("length")
        year = request.form.get("year")
        rating = request.form.get("rating")
        description = request.form.get("description")
        image = request.form.get("image")

        # Add the search terms to the search_queries dictionary if they are not empty to be used in the search_vhs function
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

        stock = request.form.get("stock")
        length = request.form.get("length")
        year = request.form.get("year")
        rating = request.form.get("rating")
        description = request.form.get("description")

        ### ADD IMAGE UPLOAD FUNCTIONALITY ###
        image = request.form.get("image")

        # Create a new vhs tape object and add it to the database with the main details provided by the user
        vhs = Videocassette(
            title=title,
            director=director,
            genre=genre,
        )

        # Create a new details object for the vhs tape and add it to the database with the additional details provided by the user
        details = Details(
            stock=stock,
            length=length,
            year=year,
            rating=rating,
            description=description,
            image=image,
        )

        # Add the vhs tape and details objects to the database
        vhs.details = details
        db.session.add(vhs)
        db.session.commit()
        return redirect(url_for("videocassettes.index"))
    return render_template("videocassettes/vhs_add.html")


@bp.route("/<id>/vhs_edit", methods=["GET", "POST"])
def vhs_edit(id):
    vhs = Videocassette.query.get(id)
    if request.method == "POST":
        # Get the vhs tape and details objects from the database and update them with the new data provided by the user
        vhs.title = request.form.get("title")
        vhs.director = request.form.get("director")
        vhs.genre = request.form.get("genre")

        vhs.details.stock = request.form.get("stock")
        vhs.details.length = request.form.get("length")
        vhs.details.year = request.form.get("year")
        vhs.details.rating = request.form.get("rating")
        vhs.details.description = request.form.get("description")
        vhs.details.image = request.form.get("image")

        db.session.commit()
        return redirect(url_for("videocassettes.index"))
    return render_template("videocassettes/vhs_edit.html", vhs=vhs)


@bp.route("/<id>/delete", methods=["GET", "POST"])
def vhs_delete(id):
    vhs = Videocassette.query.get(id)
    if request.method == "POST":
        db.session.delete(vhs)
        db.session.commit()
        return redirect(url_for("videocassettes.index"))
    return render_template("videocassettes/vhs_delete.html", vhs=vhs)
