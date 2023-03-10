from flask import session, redirect, url_for, flash, request
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("You need to be logged in to view this page.")
            return redirect(url_for("users.login", next=request.url))
        return func(*args, **kwargs)

    return wrapper
