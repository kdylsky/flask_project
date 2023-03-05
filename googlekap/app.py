from flask import Flask

app = Flask(__name__)

# 환경변수 설정
# mac
# export FLASK_APP=googlekap/app.py
# export FLASK_DEBUG=1
# flask run

# window
# set FLASK_APP="googlekap/app.py" => cmd
# set FLASK_DEBUG=1 => cmd

# $env:FLASK_APP="googlekap/app.py" => window powershell
# $env:FLASK_DEBUG=1 => window powershell
# flask run

# --port 5051 옵션


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
    return jsonify({"hello": "world"})


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


# request가 끝이 날때 동작하는 후크
@app.teardown_request
def teardown_request(exception):
    app.logger.info("teardown_request")


# app_context가 끝나는 시점에 동작하는 후크
@app.teardown_appcontext
def teardown_appcontext(exception):
    app.logger.info("teardown_appcontext")


"""Method와 request-context"""
from flask import request


@app.route("/test/method/<id>", methods=["GET", "POST"])
def method_test(id):
    return jsonify(
        {
            "request-method": request.method,
            "path-args": id,  # 패스 파라미터로 들어오는
            "request-args": request.args,  # 쿼리 파라미터로 들어오는 값
            "request-form": request.form,  # form데이터로 들어오는 값
            # "request-json": request.json #post의 body로 들어오는 값값
        }
    )


# if __name__ == "main":
#     print("run")
#     app.run(debug=True)
