from flask import Blueprint, render_template, g, redirect, url_for

NAME = "base"
# name_space, __name__
bp = Blueprint(NAME, __name__)


@bp.route("/")
def index():
    """g 컨텍스트를 이용해서"""
    if not g.user:
        return redirect(url_for("auth.login"))
    return render_template("index.html")
