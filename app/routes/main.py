from flask import Blueprint, render_template, redirect, url_for, flash, session, request


bp = Blueprint("main", __name__, url_prefix="/")

# The main route, accessible to all users, even if they are not logged in


@bp.before_request
def before_request():
    #  If the user is not logged in and tries to access a page other than the unlogged index, redirect them to the unlogged index which is accessible to all users main route.
    if not session.get("logged_in") and request.endpoint != "main.unlogged_index":
        return redirect(url_for("main.unlogged_index"))


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/unlogged_index")
def unlogged_index():
    return render_template("unlogged_index.html")
