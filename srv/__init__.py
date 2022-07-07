import locale
import os
import srv.celeryconfig

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from celery import Celery

from logging import getLogger
from srv.helpers.loader import discover_blueprints, load_models

from srv.cli import seeder_cli, scheduler_cli

app_logger = getLogger("app")
error_logger = getLogger("error")
access_logger = getLogger("access")

try:
    locale.setlocale(locale.LC_TIME, "id_ID.utf8")
except locale.Error:
    pass

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
mail = Mail()

def create_app(test: bool = False) -> Flask:
    load_models(os.path.dirname(os.path.abspath(__file__)))

    app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_object("srv.config.Config")

    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    make_cli(app)
    celery = make_celery(app)

    blueprints = discover_blueprints(os.path.dirname(os.path.abspath(__file__)))

    with app.app_context():
        for blueprint in blueprints:
            try:
                app.register_blueprint(blueprint)
            except Exception as e:
                error_logger.error(f"Failed to register blueprint {blueprint}: {e}")

        app.url_map.strict_slashes = True
        app.celery = celery
        return app

def make_cli(app: Flask) -> None:
    """
    This method use to register cli

    Arguments:
        app {Flask} -- The flask app
    """
    app.cli.add_command(seeder_cli)
    app.cli.add_command(scheduler_cli)

    @app.cli.command("check")
    def check():
        """
        This method used to check flask app
        """
        print("Everything run successfully!")

def make_celery(app: Flask):
    """
        This method used to create context task
    """
    celery = Celery(
        app.import_name,
        broker=app.config['BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.config_from_object(srv.celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
