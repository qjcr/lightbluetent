import os, subprocess, logging
from flask import Flask
from . import rooms, home, society, admins
from .flask_seasurf import SeaSurf
from flask_talisman import Talisman
from flask_babel import Babel
from .utils import gen_unique_string, ordinal, sif, page_not_found, server_error, table_exists
from lightbluetent.models import db, migrate, Setting, Role, Permission, User
import click


def create_app(config_name=None):

    if config_name == None:
        config_name = "production"

    app = Flask(__name__, template_folder="templates")

    # https://trstringer.com/logging-flask-gunicorn-the-manageable-way/
    if config_name == "production":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    config_module = f"lightbluetent.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    if not app.secret_key and "FLASK_SECRET_KEY" in os.environ:
        app.secret_key = os.environ["FLASK_SECRET_KEY"]

    if not app.request_class.trusted_hosts and "FLASK_TRUSTED_HOSTS" in os.environ:
        app.request_class.trusted_hosts = os.environ["FLASK_TRUSTED_HOSTS"].split(",")

    app.config["CSRF_CHECK_REFERER"] = False
    csrf = SeaSurf(app)
    csp = {
        "default-src": ["'self'", "www.srcf.net"],
        "img-src": ["'self'", "data:", "www.srcf.net"],
        "style-src": ["'self'", "'unsafe-inline'", "www.srcf.net"],
    }
    #Talisman(app, content_security_policy=csp)

    babel = Babel(app)

    app.jinja_env.globals["sif"] = sif
    app.jinja_env.globals["gen_unique_string"] = gen_unique_string
    app.jinja_env.globals["ordinal"] = ordinal

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(rooms.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(society.bp)
    app.register_blueprint(admins.bp)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    @app.context_processor
    def inject_gh_rev():
        return dict(
            github_rev=subprocess.check_output(["git", "describe", "--tags"])
            .strip()
            .decode()
        )

    @app.template_test()
    def equalto(value, other):
        return value == other

    @app.cli.command("change-role")
    @click.argument("crsids", nargs=-1)
    @click.argument("role", nargs=1)
    def create_user(crsids, role):
        """ Allows an admin to change a user's role """
        with app.app_context():
            for crsid in crsids:
                user = User.query.filter_by(crsid=crsid).first()
                role = Role.query.filter_by(name=role.lower()).first()
                prev_role = user.role
                if role:
                    user.role = role
                    db.session.commit()
                    click.echo(f"Changed user {user.full_name}'s role from {prev_role} to {role}")
                else:
                    click.echo("Role does not exist")

    with app.app_context():
        # create seed values for settings if not already present
        if table_exists("settings"):
            for setting in app.config["SITE_SETTINGS"]:
                has_setting = Setting.query.filter_by(name=setting["name"]).first()
                if not has_setting:
                    new_setting = Setting(name=setting["name"], enabled=setting["enabled"])
                    db.session.add(new_setting)

        if table_exists("permissions"):
            for perm in app.config["DEFAULT_PERMS"]:
                has_perm = Role.query.filter_by(name=perm["name"]).first()
                if not has_perm:
                    new_perm = Permission(name=perm["name"])
                    db.session.add(new_perm)

        if table_exists("roles"):
            for role in app.config["DEFAULT_ROLES"]:
                has_role = Role.query.filter_by(name=role["name"]).first()
                if not has_role:
                    new_role = Role(name=role["name"], description=role["description"])
                    new_role.permission = Permission.query.filter_by(
                        name=role["permission"]
                    ).first()
                    db.session.add(new_role)

        db.session.commit()

    return app
