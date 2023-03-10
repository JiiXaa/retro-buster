from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    session,
)
from app.models import Movie, VhsTapeCopy, Customer, VhsRental
from app import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.utils.utility_functions import find_movie
from app.utils.variables import MAX_RENTAL_VHS_TAPES

bp = Blueprint("movies", __name__, url_prefix="/movies")


@bp.before_request
def before_request():
    ### ADD LOGIN REQUIRED TO ALL MOVIE ROUTES ###
    if not session.get("logged_in"):
        flash("You must be logged in to view this page.")
        return redirect(url_for("users.login"))


##################################################
# Movie routes
##################################################


@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("movies/index.html")


# endpoint to get all movies from the database and pass them to the JavaScript in JSON format
@bp.route("/movies-data", methods=["GET", "POST"])
def movies_data():
    ### Passing a JSON object to JavaScript ###
    # https://stackoverflow.com/questions/42499535/passing-a-json-object-from-flask-to-javascript

    # Get all movies from the database
    movies_all = Movie.query.all()
    # Convert the movie objects to dictionaries
    movies = [movie.to_dict() for movie in movies_all]

    return jsonify(movies=movies)


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
        vhs_tapes = VhsTapeCopy.query.filter_by(movie_id=movie_id).all()
        for vhs_tape in vhs_tapes:
            if vhs_tape.is_available == False:
                flash("Cannot delete movie with tapes checked out.")
                return redirect(url_for("movies.movie_details", movie_id=movie_id))

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

            # Check if the copy number is already in database
            if VhsTapeCopy.query.filter_by(
                movie_id=movie_id, copy_number=copy_number
            ).first():
                flash("Copy number already exists. Cannot add duplicate copy.")
                return redirect(url_for("movies.vhs_add_tape", movie_id=movie_id))

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

        # Remove all rentals associated with the VhsTapeCopy object
        rentals = vhs_tape_copy.rentals
        for rental in rentals:
            # Set the rental.vhs_tape_copy to None to avoid a foreign key constraint error
            rental.vhs_tape_copy = None
            db.session.delete(rental)

        # Delete the VhsTapeCopy object from the database
        db.session.delete(vhs_tape_copy)
        db.session.commit()

        # TODO: Add archived rentals table to store rental history for deleted VHS tapes

        flash("VHS tape copy deleted successfully.")
        return redirect(url_for("movies.movie_details", movie_id=movie_id))
    return render_template(
        "videocassettes/vhs_remove.html",
        vhs_tape_copy=vhs_tape_copy,
        vhs_tape_copy_id=vhs_tape_copy_id,
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
        # Get the customer email address from the form. This might change to a customer ID in the future.
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

        # Check if the customer has already rented out the maximum number of VHS tapes
        active_rentals = [
            rental for rental in customer.rentals if not rental.date_returned
        ]

        if len(active_rentals) >= MAX_RENTAL_VHS_TAPES:
            flash("Customer has already rented out the maximum number of VHS tapes.")
            return redirect(url_for("movies.movie_details", movie_id=movie_id))

        # Check if the VHS tape is already rented by the same customer
        existing_rental = VhsRental.query.filter_by(
            vhs_tape_copy=vhs_tape_copy, customer=customer
        ).first()
        if existing_rental and existing_rental.date_returned is None:
            flash("This VHS tape is already rented by this customer.")
            return redirect(url_for("movies.movie_details", movie_id=movie_id))

        # If the VHS tape is available and not already rented by the customer,
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

        flash("VHS tape rented successfully.")
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
    movie = Movie.query.get_or_404(movie_id)
    vhs_history = VhsRental.query.filter_by(vhs_tape_copy_id=vhs_tape_copy_id).all()
    vhs_detail = VhsTapeCopy.query.filter_by(
        id=vhs_tape_copy_id, movie_id=movie_id
    ).first()
    vhs = Movie.query.filter_by(id=movie_id).first()
    today = datetime.utcnow()
    return render_template(
        "videocassettes/vhs_history.html",
        movie=movie,
        vhs=vhs,
        vhs_detail=vhs_detail,
        vhs_tape_copy_id=vhs_tape_copy_id,
        vhs_history=vhs_history,
        today=today,
    )
