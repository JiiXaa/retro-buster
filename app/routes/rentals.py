from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.rentals import VhsRental
from datetime import datetime

bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@bp.route("/", methods=["GET", "POST"])
def index():
    # TODO: Pagination would be nice here to avoid loading all rentals at once
    rentals_all = VhsRental.query.all()
    today = datetime.utcnow()

    rental_data = []

    for rental in rentals_all:
        vhs_details = rental.vhs_details
        videocassette = vhs_details.videocassette
        rental_data.append(
            {
                "id": rental.id,
                "date_rented": rental.date_rented,
                "date_returned": rental.date_returned,
                "customer_id": rental.customer_id,
                "customer_name": f"{rental.customer.first_name} {rental.customer.last_name}",
                "vhs_title": videocassette.title,
                "vhs_director": videocassette.director,
                "vhs_genre": videocassette.genre,
                "vhs_copy_number": vhs_details.copy_number,
            }
        )
    return render_template("rentals/index.html", rental_data=rental_data, today=today)
