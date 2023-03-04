# 디렉토리 안에 __init__.py가 있으면 해당 디렉토리는 파이썬 모듈화 된다.

from flask import Flask

# flask 팩토리패턴을 이용해서 순환참조 장애를 막는다.
# __init__.py에 여러개의 의존성패키지를 초기화하고 접근할 때, 순환참조 장애가 발생할 수 있다.
# 그래서 create_app안에 import구문을 넣어서 runtime시에 작동할 수 있도록 한다.
# config를 받아서 환경 별로 실행할 수 있다.
def create_app(): #config을 넣을 수 있다.
    print("run: create_app()")

    app = Flask(__name__)

    @app.route("/")
    def index():
        app.logger.info("=====index=====")
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

    """Request Hook"""
    from flask import g, current_app

    @app.before_first_request
    def before_first_request():
        app.logger.info("before_first_request")

    @app.before_request
    def before_request():
        g.test = True
        app.logger.info("before_request")

    @app.after_request
    def after_request(response):
        app.logger.info("after_request")
        app.logger.info(f"g.test:{g.test}")
        app.logger.info(f"current_app:{current_app}")
        return response

    #request가 끝이 날때 동작하는 후크
    @app.teardown_request
    def teardown_request(exception):
        app.logger.info("teardown_request")

    #app_context가 끝나는 시점에 동작하는 후크
    @app.teardown_appcontext
    def teardown_appcontext(exception):
        app.logger.info("teardown_appcontext")

    """Method와 request-context"""
    from flask import request
    @app.route("/test/method/<id>", methods=["GET","POST"])
    def method_test(id):
        return jsonify({
            "request-method": request.method,
            "path-args": id, # 패스 파라미터로 들어오는
            "request-args": request.args, #쿼리 파라미터로 들어오는 값
            "request-form": request.form, #form데이터로 들어오는 값
            # "request-json": request.json #post의 body로 들어오는 값값
        })

    return app