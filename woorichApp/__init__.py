from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
csrf = CSRFProtect()

# Flask-Login 설정
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.app_config)

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # Flask-Login 초기화
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    csrf.init_app(app)
    
    # 블루프린트
    from .views import board_views, reply_views, main_views, auth_views, mypage_views, dashboard_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(board_views.bp)
    app.register_blueprint(reply_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(mypage_views.bp)
    app.register_blueprint(dashboard_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime
    
    import jinja2
    env = jinja2.Environment()
    env.globals.update(zip=zip)
    # use env to load template(s)

    return app