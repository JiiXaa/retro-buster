from app import db
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        token = request.form.get("token")

        # Check if all fields are filled out
        if (
            not username
            or not first_name
            or not last_name
            or not email
            or not password
            or not password_confirm
            or not token
        ):
            flash("Please fill out all fields.")
            return redirect(url_for("users.register"))

        # Check if the passwords match
        if password != password_confirm:
            flash("Passwords do not match.")
            return redirect(url_for("users.register"))

        # Check if the password is at least 8 characters
        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("users.register"))

        # Check if the username is already in use
        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for("users.register"))

        # Check if the email is already in use
        if User.query.filter_by(email=email).first():
            flash("User with this email already exists.")
            return redirect(url_for("users.register"))

        if not token == "token":
            flash("Invalid token. Please contact the supervisor.")
            return redirect(url_for("users.register"))

        # Hash the password
        password_hash = generate_password_hash(password)

        # Create a new user object and add it to the database with the user details provided by the user
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash,
        )

        # Add the user object to the database and commit the changes to the database (if successful)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("User registered successfully.")
            # TODO: redirect to the user profile page / login page
            return redirect(url_for("users.register"))
        # If there is an error, rollback the changes to the database and display the error message
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__["orig"])
            flash(error)
            return redirect(url_for("users.register"))

    # If the user is not submitting a form, render the user registration form
    # query the database for all users and pass them to the template to display them on the page (for testing purposes)
    # TODO: remove this after testing
    users = User.query.all()
    return render_template("users/register.html", users=users)
