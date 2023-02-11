from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db

bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("rentals/index.html")
