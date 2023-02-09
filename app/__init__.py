import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.DevelopmentConfig")
    app.secret_key = os.environ.get("SECRET_KEY")

    app.static_folder = "static"
    app.template_folder = "templates"

    db.init_app(app)

    from app.routes.videocassettes import bp as videocassettes_bp
    from app.routes.main import bp as main_bp

    app.register_blueprint(videocassettes_bp)
    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500

    return app
