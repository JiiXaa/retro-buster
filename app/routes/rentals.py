from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.rentals import VhsRental, ArchivedRental
from datetime import datetime
from app.utils.decorators import login_required

bp = Blueprint("rentals", __name__, url_prefix="/rentals")

### Login required decorator before all requests for rentals related routes ###
@bp.before_request
@login_required
##############################################


@bp.route("/", methods=["GET", "POST"])
def index():
    # TODO: Pagination would be nice here to avoid loading all rentals at once
    rentals_all = VhsRental.query.all()
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
                "customer_name": f"{rental.customer.first_name} {rental.customer.last_name}",
                "vhs_title": movie.title,
                "vhs_director": movie.director,
                "vhs_genre": movie.genre,
                "vhs_copy_number": vhs_tape_copy.copy_number,
            }
        )
    return render_template(
        "rentals/index.html",
        rental_data=rental_data,
        today=today,
        archived_rentals=archived_rentals,
    )
