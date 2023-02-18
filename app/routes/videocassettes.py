from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Videocassette, VhsDetails
from app import db
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint("videocassettes", __name__, url_prefix="/videocassettes")

# Utility function to search for vhs tapes by title, director, or genre.
# Returns a list of vhs tapes that match the search criteria (case insensitive)
def find_vhs(search_queries):
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
    query_value = query.all()

    if not query_value:
        flash("No results found.")
    else:
        # I had to find a way to get the key and value from the dictionary and return them as a string in the flash message.
        # https://stackoverflow.com/questions/26660654/how-do-i-print-the-key-value-pairs-of-a-dictionary-in-python
        # https://stackoverflow.com/questions/58626415/turning-key-value-pairs-from-a-dictionary-into-strings

        search_strings = [
            f"{key.replace('_', ' ').title()}: {value}"
            for key, value in search_queries.items()
            if value and value.strip()
        ]
        if search_strings:
            search_message = ", ".join(search_strings)
            flash(f"Search results for: {search_message}.")
    return query.all()


@bp.route("/", methods=["GET", "POST"])
def index():
    vhs_all = Videocassette.query.all()

    ### Check that the number of copies in the database matches the total number of copies for each vhs tape ###
    ### If not, flash a message to the user to update ###
    for vhs in vhs_all:
        if len(vhs.vhs_details) < vhs.total_copies:
            flash(
                f"Copy numbers are missing {len(vhs.vhs_details)}/{vhs.total_copies} for VHS {vhs.title} - with ID: {vhs.id} please update."
            )
        elif len(vhs.vhs_details) > vhs.total_copies:
            flash(f"Too many copies for VHS {vhs.title}")

    print("vhs_all", vhs_all)
    for vhs in vhs_all:
        print("vhs.vhs_details", vhs.vhs_details)
    for vhs in vhs_all:
        print("Title:", vhs.title)
        print("Director:", vhs.director)
        print("Genre:", vhs.genre)
        print("Copy Numbers:")
    for copy in vhs.vhs_details:
        print("Copy Number:", copy.copy_number)
        print("Is Available:", copy.is_available)
        print("Available Copies:", vhs.available_copies)
    return render_template("videocassettes/index.html", vhs_all=vhs_all)


@bp.route("/vhs_search", methods=["GET", "POST"])
def vhs_search():
    if request.method == "POST":
        search_queries = {
            "title": request.form.get("title"),
            "director": request.form.get("director"),
            "genre": request.form.get("genre"),
        }
        vhs_query = find_vhs(search_queries)
        return render_template("videocassettes/vhs_found.html", vhs_query=vhs_query)
    return render_template("videocassettes/vhs_search.html")


@bp.route("/vhs_add", methods=["GET", "POST"])
def vhs_add():
    if request.method == "POST":
        title = request.form.get("title")
        director = request.form.get("director")
        genre = request.form.get("genre")
        length = request.form.get("length")
        year = request.form.get("year")
        rating = request.form.get("rating")
        description = request.form.get("description")
        total_copies = request.form.get("total_copies")
        available_copies = request.form.get("available_copies")

        ### ADD IMAGE UPLOAD FUNCTIONALITY ###
        image = request.form.get("image")

        # Check that all fields are filled out
        if not all(
            [
                title,
                director,
                genre,
                length,
                year,
                rating,
                description,
                total_copies,
                available_copies,
            ]
        ):
            flash("Please fill out all fields.")
            return redirect(url_for("videocassettes.vhs_add"))

        # Create a new vhs tape object and add it to the database with the movie details provided by the user
        vhs = Videocassette(
            title=title,
            director=director,
            genre=genre,
            length=length,
            year=year,
            rating=rating,
            description=description,
            total_copies=total_copies,
            available_copies=available_copies,
            image=image,
        )

        # Add the vhs tape object to the database
        db.session.add(vhs)
        db.session.commit()

        flash("VHS tape added successfully.")
        # Redirect to the vhs tape details page for the newly added vhs tape
        print("vhs", vhs)
        return redirect(url_for("videocassettes.vhs_add_details", vhs_id=vhs.id))
    # If the user is not submitting a form, render the vhs tape add form
    return render_template("videocassettes/vhs_add.html")


@bp.route("/vhs_edit/<id>", methods=["GET", "POST"])
def vhs_edit(id):
    vhs = Videocassette.query.get(id)
    if request.method == "POST":
        # Get the vhs tape and details objects from the database and update them with the new data provided by the user
        vhs.title = request.form.get("title")
        vhs.director = request.form.get("director")
        vhs.genre = request.form.get("genre")
        vhs.length = request.form.get("length")
        vhs.year = request.form.get("year")
        vhs.rating = request.form.get("rating")
        vhs.description = request.form.get("description")
        vhs.total_copies = request.form.get("total_copies")
        vhs.available_copies = request.form.get("available_copies")
        vhs.image = request.form.get("image")

        db.session.commit()
        return redirect(url_for("videocassettes.index"))
    return render_template("videocassettes/vhs_edit.html", vhs=vhs)


@bp.route("/<id>/delete", methods=["GET", "POST"])
def vhs_delete(id):
    vhs = Videocassette.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(vhs)
        db.session.commit()
        flash("VHS tape deleted successfully.")
        return redirect(url_for("videocassettes.index"))
    return render_template("videocassettes/vhs_delete.html", vhs=vhs)


@bp.route("/vhs_details/<id>", methods=["GET", "POST"])
def vhs_details(id):
    vhs = Videocassette.query.get_or_404(id)
    return render_template("videocassettes/vhs_details.html", vhs=vhs)


@bp.route("/vhs_add_details/<vhs_id>", methods=["GET", "POST"])
def vhs_add_details(vhs_id):
    try:
        if request.method == "POST":
            copy_number = request.form.get("copy_number")

            vhs_details = VhsDetails(
                videocassette_id=vhs_id,
                copy_number=copy_number,
                is_available=True,
            )

            db.session.add(vhs_details)
            db.session.commit()

            print("request.form", request.form)
            print(f"copy_number: {copy_number}")
            print(type(VhsDetails.copy_number))

            flash("VHS tape details added successfully.")
            return redirect(url_for("videocassettes.vhs_add_details", vhs_id=vhs_id))

        vhs = Videocassette.query.get_or_404(vhs_id)
        print("vhs", vhs)
        return render_template("videocassettes/vhs_add_details.html", vhs=vhs)
    except SQLAlchemyError as e:
        db.session.rollback()
        error = str(e.__dict__.get("orig") or e)
        flash(f"An error occurred: {error}", "error")
        return redirect(url_for("videocassettes.vhs_add_details", vhs_id=vhs_id))
