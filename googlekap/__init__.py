# 디렉토리 안에 __init__.py가 있으면 해당 디렉토리는 파이썬 모듈화 된다.

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
# flask 팩토리패턴을 이용해서 순환참조 장애를 막는다.
# __init__.py에 여러개의 의존성패키지를 초기화하고 접근할 때, 순환참조 장애가 발생할 수 있다.
# 그래서 create_app안에 import구문을 넣어서 runtime시에 작동할 수 있도록 한다.
# config를 받아서 환경 별로 실행할 수 있다.
def create_app():  # config을 넣을 수 있다.
    print("run: create_app()")

    app = Flask(__name__)

    app.config["SECRET_KEY"]="secretkey"
    app.config["SESSION_COOKIE_NAME"] = "googlekap_session"
    if app.config["DEBUG"]:
        app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1

    """CSRF INIT"""
    csrf.init_app(app)

    """Routes INIT"""
    from googlekap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)

    @app.errorhandler(404)
    def page_404(error):
        return render_template("/404.html"), 404

    return app
