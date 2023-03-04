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

# if __name__ == "main":
#     print("run")
#     app.run(debug=True)