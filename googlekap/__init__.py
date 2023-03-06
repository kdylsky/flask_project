# 디렉토리 안에 __init__.py가 있으면 해당 디렉토리는 파이썬 모듈화 된다.

from flask import Flask, render_template, g
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

# flask 팩토리패턴을 이용해서 순환참조 장애를 막는다.
# __init__.py에 여러개의 의존성패키지를 초기화하고 접근할 때, 순환참조 장애가 발생할 수 있다.
# 그래서 create_app안에 import구문을 넣어서 runtime시에 작동할 수 있도록 한다.
# config를 받아서 환경 별로 실행할 수 있다.
def create_app(config=None):  # config을 넣을 수 있다.
    print("run: create_app()")

    app = Flask(__name__)

    """Flask Configs"""
    from .configs import DevelopmentConfig, ProductionConfig
    if not config:
        if app.config["DEBUG"]:
            config = DevelopmentConfig()
        else:
            config = ProductionConfig()
    app.config.from_object(config)

    """CSRF INIT"""
    csrf.init_app(app)

    """DB INIT"""
    db.init_app(app)
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    """Routes INIT"""
    from googlekap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)

    """Restx INIT"""
    from googlekap.apis import blueprint as api
    app.register_blueprint(api)


    """REQUEST HOOK"""
    @app.before_request
    def before_request():
        g.db = db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, "db"):
            g.db.close()

    @app.errorhandler(404)
    def page_404(error):
        return render_template("/404.html"), 404

    return app
