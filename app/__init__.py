import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CsrfProtect(app)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
# bootstrap needs to be last for bootstraop styling to take effect
bootstrap = Bootstrap(app)


from app.errors import bp as errors_bp  # noqa: E402 F401
app.register_blueprint(errors_bp)


from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)


from app.main import bp as main_bp
app.register_blueprint(main_bp)


if not app.debug:
    # ...

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/receipt.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Receipt startup')
