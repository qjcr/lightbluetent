import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""

    user = os.getenv("POSTGRES_USER", "qjcr")
    password = os.getenv("POSTGRES_PASSWORD")
    hostname = os.getenv("POSTGRES_HOSTNAME", "localhost")
    port = int(os.getenv("POSTGRES_PORT", 5432))
    database = os.getenv("APPLICATION_DB", "lightbluetent")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_URI", f"postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Requests up to 1 MB
    MAX_CONTENT_LENGTH = 1024 * 1024

    HAS_DIRECTORY_PAGE = True
    NUMBER_OF_DAYS = 1

    DEFAULT_LOGO = "default_logo.png"
    DEFAULT_BBB_LOGO = "default_bbb_logo.png"
    MAX_LOGO_SIZE = (512, 512)
    LOGO_ALLOWED_EXTENSIONS = {".png", ".jpeg", ".jpg", ".gif"}
    IMAGES_DIR = "lightbluetent/static/images"

    # Since using url_for(static", ...) prepends lightbluetent/static to the URL
    # for us, we have the relative path to the images directory from the static folder.
    # I couldn't think of a better way of doing this. Required in society.py for
    # getting the URL of the bbb_logo to pass to BBB.
    IMAGES_DIR_FROM_STATIC = "images"





class ProductionConfig(Config):
    """Production configuration"""


class DevelopmentConfig(Config):
    """Development configuration"""


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
