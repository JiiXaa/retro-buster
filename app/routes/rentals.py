from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.rentals import VhsRental, ArchivedRental
from app.models.movies import VhsTapeCopy
from datetime import datetime

bp = Blueprint("rentals", __name__, url_prefix="/rentals")

### Login required decorator before all requests for rentals related routes ###
@bp.before_request
def before_request():
    ### ADD LOGIN REQUIRED TO ALL MOVIE ROUTES ###
    if not session.get("logged_in"):
        flash("You must be logged in to view this page.")
        return redirect(url_for("users.login"))


##############################################


@bp.route("/", methods=["GET", "POST"])
def index():
    # TODO: Pagination would be nice here to avoid loading all rentals at once

    # Rentals are ordered by date_rented descending
    rentals_all = VhsRental.query.order_by(VhsRental.date_rented.desc()).all()
    today = datetime.utcnow()

    archived_rentals = ArchivedRental.query.all()

    rental_data = []

    for rental in rentals_all:
        vhs_tape_copy = rental.vhs_tape_copy
        movie = vhs_tape_copy.movie
        rental_data.append(
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
                "vhs_copy_number": vhs_tape_copy.copy_number,
                "due_date": rental.due_date,
            }
        )
    return render_template(
        "rentals/index.html",
        rental_data=rental_data,
        today=today,
        archived_rentals=archived_rentals,
    )


@bp.route("/archived_rentals", methods=["GET"])
def archived_rentals():
    vhs_tape_copies = VhsTapeCopy.query.filter(VhsTapeCopy.is_removed == True).all()
    print("archived_rentals", vhs_tape_copies)

    return render_template(
        "rentals/archived_rentals.html", vhs_tape_copies=vhs_tape_copies
    )
