import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

db = SQLAlchemy()
load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.ProductionConfig")
    app.secret_key = os.environ.get("SECRET_KEY")
    app.static_folder = "static"
    app.template_folder = "templates"

    db.init_app(app)
    # Used Flask-Migrate documentation to set up and use migrations in the project: https://flask-migrate.readthedocs.io/en/latest/
    migrate = Migrate(app, db)

    from app.routes.users import bp as users_bp
    from app.routes.main import bp as main_bp
    from app.routes.movies import bp as movies_bp
    from app.routes.customers import bp as customers_bp
    from app.routes.rentals import bp as rentals_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(rentals_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500

    return app
