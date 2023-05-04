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
from app.models import Movie, VhsTapeCopy, Customer, VhsRental, ArchivedRental, User
from app import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from sqlalchemy import and_
import math
from datetime import datetime, timedelta
from app.utils.utility_functions import find_movie
from app.utils.variables import (
    MAX_RENTAL_VHS_TAPES,
    MAX_RENTAL_DAYS,
    FEATURED_MOVIES_COUNT,
)

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


# endpoint to get all movies from the database and pass them to the JavaScript in JSON format (for pagination)
MOVIES_PER_PAGE = 8


@bp.route("/movies-data", methods=["GET", "POST"])
def movies_data():
    # Get the current page from query parameters (default to 1 if not provided)
    page = int(request.args.get("page", 1))

    # Calculate the offset for the query
    offset = (page - 1) * MOVIES_PER_PAGE

    # Get the total number of movies in the database
    total_movies = Movie.query.count()

    # Calculate the total number of pages
    total_pages = math.ceil(total_movies / MOVIES_PER_PAGE)

    # Get the movies for the current page using limit and offset
    movies_page = Movie.query.limit(MOVIES_PER_PAGE).offset(offset).all()

    # Convert the movie objects to dictionaries
    movies = [movie.to_dict() for movie in movies_page]

    # Return the movies, current page, and total pages as a JSON object
    return jsonify(movies=movies, current_page=page, total_pages=total_pages)


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


@bp.route("/featured_movies", methods=["GET"])
def featured_movies():
    # Find the 10 movies with is_featured set to True
    get_featured_movies = Movie.query.filter(Movie.is_featured == True).limit(10).all()

    # Create a set of movie IDs to keep track of the movies already added
    added_movie_ids = {movie.id for movie in get_featured_movies}

    # If there are less than 10 movies with is_featured set to True, find the most rented movies
    if len(get_featured_movies) < FEATURED_MOVIES_COUNT:
        all_movies = Movie.query.all()
        most_rented_movies = sorted(
            all_movies, key=lambda movie: movie.rental_count(), reverse=True
        )

        # Add the most rented movies to the list of featured movies, only if they are not already added
        for movie in most_rented_movies:
            if len(get_featured_movies) >= FEATURED_MOVIES_COUNT:
                break
            if movie.id not in added_movie_ids:
                get_featured_movies.append(movie)
                added_movie_ids.add(movie.id)

    # Convert the movie objects to dictionaries and pass them to the JavaScript in JSON format
    featured_movies = [movie.to_dict() for movie in get_featured_movies]

    return jsonify(featured_movies=featured_movies)


@bp.route("/movies_due_today", methods=["GET"])
def movies_due_today():
    today = datetime.utcnow().date()

    # Get all movies that are due today. Used func.date() to convert the due_date column to a date object
    due_today = VhsRental.query.filter(
        and_(
            func.date(VhsRental.due_date) == today,
            (VhsRental.date_returned.is_(None)),
        )
    ).all()

    movies_due_today = [movie.movie.to_dict() for movie in due_today]

    return jsonify(movies_due_today=movies_due_today)


@bp.route("/movie_add", methods=["GET", "POST"])
def movie_add():
    if request.method == "POST":
        title = request.form.get("title").strip().lower()
        director = request.form.get("director").strip().lower()
        genre = request.form.get("genre").strip().lower()
        length = request.form.get("length").strip()
        year = request.form.get("year").strip()
        rating = request.form.get("rating").strip()
        description = request.form.get("description").strip()
        is_featured = bool(request.form.get("is_featured"))

        ### ADD IMAGE UPLOAD FUNCTIONALITY ###
        image = request.form.get("image").strip()

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
            is_featured=is_featured,
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
        movie.title = request.form.get("title").strip().lower()
        movie.director = request.form.get("director").strip().lower()
        movie.genre = request.form.get("genre").strip().lower()
        movie.length = request.form.get("length").strip()
        movie.year = request.form.get("year").strip()
        movie.rating = request.form.get("rating").strip()
        movie.description = request.form.get("description").strip()
        movie.image = request.form.get("image").strip()
        movie.is_featured = bool(request.form.get("is_featured"))

        db.session.commit()
        flash("Movie updated successfully.")
        return redirect(url_for("movies.movie_details", movie_id=movie_id))
    return render_template("movies/movie_edit.html", movie=movie)


@bp.route("/movie_delete/<movie_id>", methods=["GET", "POST"])
def movie_delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title_confirm = request.form.get("title_confirm").strip().lower()
        if title_confirm != movie.title:
            flash("Movie title does not match.")
            return redirect(url_for("movies.movie_delete", movie_id=movie_id))
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
            copy_number = request.form.get("copy_number").strip().lower()

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
                user_id=session["user_id"],
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
    user = User.query.get_or_404(session.get("user_id"))

    if request.method == "POST":
        vhs_confirm = request.form.get("vhs_title_confirm").strip().lower()
        if vhs_confirm != movie.title:
            flash("Movie title does not match.")
            return redirect(
                url_for(
                    "movies.vhs_remove",
                    movie_id=movie.id,
                    vhs_tape_copy_id=vhs_tape_copy.id,
                )
            )
        try:
            archived_rentals = []

            # Remove all rentals associated with the VhsTapeCopy object
            if vhs_tape_copy.rentals:
                for rental in vhs_tape_copy.rentals:
                    # Create a new ArchivedRental object and add it to the database before deleting the Rental object
                    archived_rental = ArchivedRental(
                        date_rented=rental.date_rented,
                        date_returned=rental.date_returned,
                        date_archived=datetime.utcnow(),
                        user_id=user.id,
                        customer_id=rental.customer_id,
                        vhs_tape_copy_id=rental.vhs_tape_copy_id,
                        movie_id=rental.movie_id,
                    )
                    archived_rentals.append(archived_rental)
                    # Set the is_removed flag to True so that the Rental object is not deleted from the database, this is so that the ArchivedRental object can be created and avoid a foreign key constraint error.
                    rental.is_removed = True

            # Set the is_removed flag to True so that the VhsTapeCopy object is not deleted from the database, this is so that the ArchivedRental object can be created and avoid a foreign key constraint error.
            vhs_tape_copy.is_removed = True
            db.session.commit()

            # Add archived rentals to the database
            # Stumbled upon this solution to add multiple objects to the database at once: https://stackoverflow.com/questions/58517491/sqlalchemy-bulk-save-objects-vs-add-all-underlying-logic-difference
            # Remember: Keep in mind that using bulk_save_objects will bypass some SQLAlchemy features like automatically populating default values, cascades, and events. Make sure to handle those aspects in your code if needed.
            db.session.bulk_save_objects(archived_rentals)
            db.session.commit()

            flash("VHS tape copy deleted successfully.")
            return redirect(url_for("movies.movie_details", movie_id=movie_id))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while deleting VHS tape copy: " + str(e), "error")
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
        customer_query = request.form.get("customer_query").strip().lower()
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
            due_date=datetime.utcnow() + timedelta(days=MAX_RENTAL_DAYS),
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

    if rental.due_date < datetime.utcnow():
        rental.is_late = True
        flash("VHS tape returned late.")
    else:
        rental.is_late = False
        flash("VHS tape returned on time.")

    vhs_tape_copy.is_available = True
    db.session.commit()

    flash("VHS returned successfully.")
    return redirect(url_for("movies.movie_details", movie_id=movie_id))


@bp.route("/vhs_history/<movie_id>/<vhs_tape_copy_id>", methods=["GET", "POST"])
def vhs_history(movie_id, vhs_tape_copy_id):
    movie = Movie.query.get_or_404(movie_id)
    vhs_rentals = VhsRental.query.filter_by(vhs_tape_copy_id=vhs_tape_copy_id).all()
    vhs_detail = VhsTapeCopy.query.filter_by(
        id=vhs_tape_copy_id, movie_id=movie_id
    ).first()
    vhs = Movie.query.filter_by(id=movie_id).first()
    today = datetime.utcnow()

    vhs_history_data = []

    for rental in vhs_rentals:
        vhs_history_data.append(
            {
                "id": rental.id,
                "date_rented": rental.date_rented,
                "date_returned": rental.date_returned,
                "is_removed": rental.is_removed,
                "customer_id": rental.customer_id,
                "customer_name": f"{rental.customer.first_name} {rental.customer.last_name}"
                if rental.customer
                else "Customer not found",
                "vhs_title": movie.title,
                "vhs_director": movie.director,
                "vhs_genre": movie.genre,
                "vhs_copy_number": vhs_detail.copy_number,
                "due_date": rental.due_date,
            }
        )

    return render_template(
        "videocassettes/vhs_history.html",
        movie=movie,
        vhs=vhs,
        vhs_detail=vhs_detail,
        vhs_history_data=vhs_history_data,
        today=today,
    )
