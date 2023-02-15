from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Customer
from app import db

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
    value = query.all()

    if not value:
        flash("No results found.")
    else:
        flash(f"Search results for: '{''.join(search_queries.values())}'.")
    return query.all()


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
