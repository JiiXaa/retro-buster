from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Movie, VhsTapeCopy, Customer, VhsRental
from app import db
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

bp = Blueprint("movies", __name__, url_prefix="/movies")

##################################################
# Utility function to search for movies by title, director, or genre.
# Returns a list of movies that match the search criteria (case insensitive)
##################################################
def find_movie(search_queries):
    if not search_queries:
        flash("Please provide at least one search term.")

    query = Movie.query
    for term in search_queries:
        if term == "title":
            query = query.filter(Movie.title.ilike("%" + search_queries[term] + "%"))
        elif term == "director":
            query = query.filter(Movie.director.ilike("%" + search_queries[term] + "%"))
        elif term == "genre":
            query = query.filter(Movie.genre.ilike("%" + search_queries[term] + "%"))
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


##################################################
# Movie routes
##################################################


@bp.route("/", methods=["GET", "POST"])
def index():
    movies_all = Movie.query.all()

    return render_template("movies/index.html", movies_all=movies_all)


@bp.route("/movie_search", methods=["GET", "POST"])
def movie_search():
    if request.method == "POST":
        search_queries = {
            "title": request.form.get("title"),
            "director": request.form.get("director"),
            "genre": request.form.get("genre"),
        }

        if all(value == "" for value in search_queries.values()):
            flash("Please provide at least one search term.")
            return redirect(url_for("movies.movie_search"))
        movie_query = find_movie(search_queries)
        return render_template("movies/movie_found.html", movie_query=movie_query)
    return render_template("movies/movie_search.html")


@bp.route("/movie_add", methods=["GET", "POST"])
def movie_add():
    if request.method == "POST":
        title = request.form.get("title")
        director = request.form.get("director")
        genre = request.form.get("genre")
        length = request.form.get("length")
        year = request.form.get("year")
        rating = request.form.get("rating")
        description = request.form.get("description")

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
            ]
        ):
            flash("Please fill out all fields.")
            return redirect(url_for("movies.movie_add"))

        # Create a new movie object and add it to the database with the details provided by the user
        movie = Movie(
            title=title,
            director=director,
            genre=genre,
            length=length,
            year=year,
            rating=rating,
            description=description,
            image=image,
        )

        # Add the movie tape object to the database
        db.session.add(movie)
        db.session.commit()

        flash("Movie added successfully.")
        # Redirect to the movie details page to add a tape copy
        return redirect(url_for("movies.vhs_add_tape", movie_id=movie.id))
    # If the user is not submitting a form, render the vhs tape add form
    return render_template("movies/movie_add.html")


@bp.route("/movie_edit/<movie_id>", methods=["GET", "POST"])
def movie_edit(movie_id):
    movie = Movie.query.get(movie_id)
    if request.method == "POST":
        # Get the movie and tape copy objects from the database and update them with the new data provided by the user
        movie.title = request.form.get("title")
        movie.director = request.form.get("director")
        movie.genre = request.form.get("genre")
        movie.length = request.form.get("length")
        movie.year = request.form.get("year")
        movie.rating = request.form.get("rating")
        movie.description = request.form.get("description")
        movie.image = request.form.get("image")

        db.session.commit()
        return redirect(url_for("movies.index"))
    return render_template("movies/movie_edit.html", movie=movie)


@bp.route("/movie_delete/<movie_id>", methods=["GET", "POST"])
def movie_delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        # Delete the Movie object from the database
        db.session.delete(movie)
        db.session.commit()

        flash("Movie deleted successfully.")
        return redirect(url_for("movies.index"))
    return render_template("movies/movie_delete.html", movie=movie)


@bp.route("/movie_details/<movie_id>", methods=["GET", "POST"])
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template("movies/movie_details.html", movie=movie)


##################################################
# VHS Tape routes
##################################################


@bp.route("/vhs_add_tape/<movie_id>", methods=["GET", "POST"])
def vhs_add_tape(movie_id):
    try:
        if request.method == "POST":
            copy_number = request.form.get("copy_number")

            vhs_tape_copy = VhsTapeCopy(
                movie_id=movie_id,
                copy_number=copy_number,
                is_available=True,
            )

            db.session.add(vhs_tape_copy)
            db.session.commit()

            flash("VHS tape copy added successfully.")
            return redirect(url_for("movies.vhs_add_tape", movie_id=movie_id))

        movie = Movie.query.get_or_404(movie_id)

        return render_template("videocassettes/vhs_add_tape.html", movie=movie)
    except SQLAlchemyError as e:
        db.session.rollback()
        error = str(e.__dict__.get("orig") or e)
        flash(f"An error occurred: {error}", "error")
        return redirect(url_for("videocassettes.vhs_add_tape", movie_id=movie_id))


@bp.route("/vhs_remove/<movie_id>/<vhs_tape_copy_id>", methods=["GET", "POST"])
def vhs_remove(movie_id, vhs_tape_copy_id):
    vhs_tape_copy = VhsTapeCopy.query.get_or_404(vhs_tape_copy_id)
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        # Delete the VhsTapeCopy object from the database
        db.session.delete(vhs_tape_copy)
        db.session.commit()

        flash("VHS tape copy deleted successfully.")
        return redirect(url_for("movies.movie_details", movie_id=movie_id))
    return render_template(
        "videocassettes/vhs_remove.html",
        vhs_tape_copy=vhs_tape_copy,
        movie=movie,
        movie_id=movie_id,
    )


@bp.route("/vhs_rent/<movie_id>/rent_copy/<vhs_tape_copy_id>", methods=["GET", "POST"])
def vhs_rent(movie_id, vhs_tape_copy_id):
    # Get the vhs copy tape object from the database
    vhs_tape_copy = VhsTapeCopy.query.filter_by(id=vhs_tape_copy_id).first()
    if not vhs_tape_copy:
        flash("Invalid VHS tape selected.")
        return redirect(url_for("movies.index"))

    # Find the customer in the database
    if request.method == "POST":
        customer_query = request.form.get("customer_query")
        if not customer_query:
            flash("Please enter a customer email address.")
            return redirect(
                url_for(
                    "videocassettes.vhs_rent",
                    movie_id=movie_id,
                    vhs_tape_copy_id=vhs_tape_copy_id,
                )
            )

        customer = Customer.query.filter_by(email=customer_query).first()
        if not customer:
            flash("Customer not found")
            return redirect(
                url_for(
                    "customers.customer_add",
                )
            )

        # Check if the vhs tape is available
        if not vhs_tape_copy.is_available:
            flash("VHS tape is not available.")
            return redirect(url_for("movies.movie_details", movie_id=movie_id))

        # Check if the VHS tape is already rented by the same customer
        existing_rental = VhsRental.query.filter_by(
            vhs_tape_copy=vhs_tape_copy, customer=customer
        ).first()
        if existing_rental and existing_rental.date_returned is None:
            flash("This VHS tape is already rented by this customer.")
            return redirect(url_for("movies.movie_details", movie_id=movie_id))

        # If the VHS tape is available and not already rented by the same customer,
        # set the is_available field to False
        vhs_tape_copy.is_available = False

        # Get the corresponding movie object and set the movie_id attribute
        movie = Movie.query.filter_by(id=movie_id).first()

        # Create a new rental object and set the movie_id attribute
        rental = VhsRental(
            date_rented=datetime.utcnow(),
            vhs_tape_copy=vhs_tape_copy,
            customer=customer,
            movie=movie,
        )
        db.session.add(rental)
        db.session.commit()

        flash("Rental created successfully.")
        return redirect(url_for("movies.movie_details", movie_id=movie_id))

    return render_template(
        "videocassettes/vhs_rent.html",
        vhs_tape_copy=vhs_tape_copy,
    )


@bp.route("/vhs_return/<movie_id>/<vhs_tape_copy_id>", methods=["GET", "POST"])
def vhs_return(movie_id, vhs_tape_copy_id):
    # Get the vhs copy tape object from the database
    vhs_tape_copy = VhsTapeCopy.query.filter_by(
        id=vhs_tape_copy_id, movie_id=movie_id
    ).first()
    if not vhs_tape_copy:
        flash("Invalid VHS tape selected.")
        return redirect(url_for("movies.index"))

    # Find the rental object in the database and check if it has already been returned
    rental = VhsRental.query.filter_by(
        vhs_tape_copy_id=vhs_tape_copy_id, date_returned=None
    ).first()
    if not rental:
        flash("VHS tape is not rented.")
        return redirect(url_for("movies.movie_details", movie_id=movie_id))
    elif rental.date_returned is not None:
        flash("VHS tape has already been returned.")
        return redirect(url_for("movies.movie_details", movie_id=movie_id))

    # Update the VhsRental and VhsTapeCopy objects
    rental.date_returned = datetime.utcnow()
    vhs_tape_copy.is_available = True
    db.session.commit()

    flash("VHS returned successfully.")
    return redirect(url_for("movies.movie_details", movie_id=movie_id))


@bp.route("/vhs_history/<movie_id>/<vhs_tape_copy_id>", methods=["GET", "POST"])
def vhs_history(movie_id, vhs_tape_copy_id):
    vhs_history = VhsRental.query.filter_by(vhs_tape_copy_id=vhs_tape_copy_id).all()
    vhs_detail = VhsTapeCopy.query.filter_by(
        id=vhs_tape_copy_id, movie_id=movie_id
    ).first()
    vhs = Movie.query.filter_by(id=movie_id).first()
    today = datetime.utcnow()
    return render_template(
        "videocassettes/vhs_history.html",
        vhs=vhs,
        vhs_detail=vhs_detail,
        vhs_tape_copy_id=vhs_tape_copy_id,
        vhs_history=vhs_history,
        today=today,
    )
