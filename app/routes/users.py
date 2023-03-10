from app import db
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from app.utils.decorators import login_required

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Verify the user's credentials
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if all fields are filled out
        if not username or not password:
            flash("Please fill out all fields.")
            return redirect(url_for("users.login"))

        # Check if the user exists or password is correct
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("Invalid username or password.")
            return redirect(url_for("users.login"))
        password_hashed = check_password_hash(user.password_hash, password)
        if not user or not password_hashed:
            flash("Invalid username or password.")
            return redirect(url_for("users.login"))

        # log the user in / set session variables
        session["logged_in"] = True
        session["username"] = user.username

        flash(f"Welcome, {user.username.capitalize()}")
        return redirect(url_for("users.dashboard", username=user.username))

    return render_template("users/login.html")


@bp.route("/logout")
def logout():
    # Clear session variables
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("users.login"))


@bp.route("/dashboard/<username>")
# dashboard route is protected by the login_required decorator
@login_required
def dashboard(username):
    # Check if the user is logged in
    if not session.get("logged_in"):
        flash("Please log in to view the dashboard.")
        return redirect(url_for("users.login"))
    else:
        username = session.get("username")
        user = User.query.filter_by(username=username).first()
        return render_template("users/dashboard.html", user=user)


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
            return redirect(url_for("users.login"))
        except SQLAlchemyError as e:
            # If there is an error, rollback the changes to the database and display the error message
            db.session.rollback()
            error = str(e.__dict__["orig"])
            flash(error)
            return redirect(url_for("users.register"))

    # If the user is not submitting a form, render the user registration form
    # query the database for all users and pass them to the template to display them on the page (for testing purposes)
    # TODO: remove this after testing
    users = User.query.all()
    return render_template("users/register.html", users=users)
