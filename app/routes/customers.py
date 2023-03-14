from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Customer, Movie, VhsTapeCopy, VhsRental
from app import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.utils.utility_functions import find_customer
from app.utils.variables import MAX_RENTAL_VHS_TAPES


bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.before_request
def before_request():
    ### ADD LOGIN REQUIRED TO ALL CUSTOMERS ROUTES ###
    if not session.get("logged_in"):
        flash("You must be logged in to view this page.")
        return redirect(url_for("users.login"))


##############################################


@bp.route("/", methods=["GET", "POST"])
def index():
    customers_all = Customer.query.all()
    print("customers_all", customers_all)
    return render_template("customers/index.html", customers_all=customers_all)


@bp.route("/customer_search", methods=["GET", "POST"])
def customer_search():
    if request.method == "POST":
        search_queries = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
        }
        customer_query = find_customer(search_queries)

        if all(value == "" for value in search_queries.values()):
            flash("Please provide at least one search term.")
            return redirect(url_for("customers.customer_search"))
        return render_template(
            "customers/customer_found.html", customer_query=customer_query
        )
    return render_template("customers/customer_search.html")


@bp.route("/customer_add", methods=["GET", "POST"])
def customer_add():
    # If the user is submitting a form, add the customer to the database
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")

        # Check that all fields are filled out
        if not all([first_name, last_name, email]):
            flash("Please fill out all fields.")
            return redirect(url_for("customers.customer_add"))

        # Create a new customer object and add it to the database with the customer details provided by the user
        customer = Customer(first_name=first_name, last_name=last_name, email=email)

        # Check if the customer already exists in the database
        ### found solution here: https://stackoverflow.com/questions/32938475/flask-sqlalchemy-check-if-row-exists-in-table
        is_existing_customer = Customer.query.filter_by(email=email).first()
        if is_existing_customer:
            flash("Customer already exists.")
            return redirect(url_for("customers.customer_add"))

        # Add the customer object to the database
        db.session.add(customer)
        db.session.commit()

        flash("Customer added successfully.")
        # Redirect to the customer profile page
        return redirect(url_for("customers.customer_profile", customer_id=customer.id))
    # If the user is not submitting a form, render the customer add form
    return render_template("customers/customer_add.html")


@bp.route("/customer_edit/<customer_id>", methods=["GET", "POST"])
def customer_edit(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == "POST":
        customer.first_name = request.form.get("first_name")
        customer.last_name = request.form.get("last_name")
        customer.email = request.form.get("email")

        # Check that all fields are filled out
        if not all([customer.first_name, customer.last_name, customer.email]):
            flash("Please fill out all fields.")
            return redirect(url_for("customers.customer_edit", customer_id=customer.id))

        db.session.commit()
        flash("Customer updated successfully.")
        return redirect(url_for("customers.index"))
    return render_template("customers/customer_edit.html", customer=customer)


@bp.route("customer_delete/<customer_id>", methods=["GET", "POST"])
def customer_delete(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == "POST":
        db.session.delete(customer)
        db.session.commit()
        flash("Customer deleted successfully.")
        return redirect(url_for("customers.index"))
    return render_template("customers/customer_delete.html", customer=customer)


@bp.route("/customer_profile/<customer_id>", methods=["GET", "POST"])
def customer_profile(customer_id):
    # TODO: Add a form to edit the customer's information
    # TODO: Add a form to delete the customer's account

    # Fetch the customer object from the database
    customer = Customer.query.get_or_404(customer_id)

    return render_template(
        "customers/customer_profile.html",
        customer=customer,
    )


@bp.route("/customer_profile/<customer_id>/vhs_rent", methods=["POST"])
def customer_vhs_rent(customer_id):
    # Get the movie ID and VHS tape copy ID from the form
    movie_title = request.form.get("movie_title")
    vhs_copy_number = request.form.get("vhs_copy_number")

    # Get the VHS tape copy object from the database
    vhs_tape_copy = VhsTapeCopy.query.filter_by(copy_number=vhs_copy_number).first()
    if not vhs_tape_copy:
        flash("VHS tape copy not found.")
        return redirect(url_for("customers.customer_profile", customer_id=customer_id))

    # Get the customer object from the database
    customer = Customer.query.get_or_404(customer_id)
    if not customer:
        flash("Customer not found.")
        return redirect(url_for("customers.customer_profile", customer_id=customer_id))

    # Check if the VHS tape copy is already rented out
    if not vhs_tape_copy.is_available:
        flash("VHS tape copy is already rented out.")
        return redirect(url_for("customers.customer_profile", customer_id=customer_id))

    # Check if the customer has already rented out the maximum number of VHS tapes
    active_rentals = [rental for rental in customer.rentals if not rental.date_returned]

    if len(active_rentals) >= MAX_RENTAL_VHS_TAPES:
        flash("Customer already rented out the maximum number of VHS tapes.")
        return redirect(url_for("customers.customer_profile", customer_id=customer_id))

    # If the VHS tape is available and not already rented by the customer,
    # set the is_available field to False
    vhs_tape_copy.is_available = False

    # Get the movie object from the database
    movie = Movie.query.filter_by(title=movie_title).first()

    # Create a new rental object and add it to the database
    rental = VhsRental(
        date_rented=datetime.now(),
        vhs_tape_copy=vhs_tape_copy,
        customer=customer,
        movie=movie,
    )
    db.session.add(rental)
    db.session.commit()

    flash("VHS tape rented successfully.")
    return redirect(url_for("customers.customer_profile", customer_id=customer_id))
