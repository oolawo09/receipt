from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CsrfProtect(app)
login = LoginManager(app)
login.login_view = 'login'
# bootstrap needs to be last for bootstraop styling to take effect
bootstrap = Bootstrap(app)


from app import routes, models, errors  # noqa: E402 F401
