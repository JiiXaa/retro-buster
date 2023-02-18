from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Customer
from app import db
from sqlalchemy.exc import SQLAlchemyError


bp = Blueprint("customers", __name__, url_prefix="/customers")

# Utility function to search for customer by first_name, last_name, or email.
# Returns a list of customers that match the search criteria (case insensitive)
def find_customer(search_queries):
    if not search_queries:
        flash("Please provide at least one search term.")

    query = Customer.query
    for term in search_queries:
        if term == "first_name":
            query = query.filter(
                Customer.first_name.ilike("%" + search_queries[term] + "%")
            )
        elif term == "last_name":
            query = query.filter(
                Customer.last_name.ilike("%" + search_queries[term] + "%")
            )
        elif term == "email":
            query = query.filter(Customer.email.ilike("%" + search_queries[term] + "%"))
    query_value = query.all()

    if not query_value:
        flash("No results found.")
    else:
        print("search_queries.values()", search_queries.values())
        print("search_queries.items()", search_queries.items())
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
    return query_value


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


@bp.route("/customer_profile/<customer_id>", methods=["GET", "POST"])
def customer_profile(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        print("customer", customer)

        return render_template("customers/customer_profile.html", customer=customer)
    except SQLAlchemyError as e:
        db.session.rollback()
        error = str(e.__dict__.get("orig") or e)
        flash(f"An error occurred: {error}", "error")
        return redirect(url_for("customers.index"))
