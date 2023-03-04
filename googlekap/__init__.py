# 디렉토리 안에 __init__.py가 있으면 해당 디렉토리는 파이썬 모듈화 된다.

from flask import Flask, current_app

# flask 팩토리패턴을 이용해서 순환참조 장애를 막는다.
# __init__.py에 여러개의 의존성패키지를 초기화하고 접근할 때, 순환참조 장애가 발생할 수 있다.
# 그래서 create_app안에 import구문을 넣어서 runtime시에 작동할 수 있도록 한다.
# config를 받아서 환경 별로 실행할 수 있다.
def create_app(): #config을 넣을 수 있다.
    print("run: create_app()")

    app = Flask(__name__)

    @app.route("/")
    def index():
        return "hello world"

    """Routing"""
    from flask import jsonify, redirect, url_for
    @app.route("/test/name/<name>")
    def name(name):
        return f"Name is {name}"

    @app.route("/test/id/<int:id>")
    def id(id):
        return f"id is {id}"

    @app.route("/test/path/<path:subpath>")
    def path(subpath):
        return subpath

    @app.route("/test/json")
    def json():
        return jsonify({"hello":"world"})

    @app.route("/test/redirect/<path:subpath>")
    def redirct_url(subpath):
        return redirect(subpath)

    @app.route("/test/url-for/<path:subpath>")
    def urlfor(subpath):
        return redirect(url_for("path", subpath=subpath))

    return app