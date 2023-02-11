from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Customer
from app import db

bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.route("/", methods=["GET", "POST"])
def index():
    customers_all = Customer.query.all()
    print("customers_all", customers_all)
    return render_template("customers/index.html", customers_all=customers_all)
