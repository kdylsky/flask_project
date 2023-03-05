from flask import Blueprint, render_template

NAME = "base"
# name_space, __name__
bp = Blueprint(NAME, __name__)

@bp.route("/")
def index():
    return render_template("index.html")
