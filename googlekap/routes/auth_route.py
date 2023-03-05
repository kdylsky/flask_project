from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from googlekap.forms.auth_form import LoginFrom, RegisterFrom

NAME = "auth"
bp = Blueprint(NAME, __name__, url_prefix="/auth")

# 메모리에 유저데이터 테스트
"""testing"""
from dataclasses import dataclass
user_list = []

@dataclass
class User:
    user_id: str
    user_name: str
    password: str

user_list.append(User("tester1_id", "tester1_name", "tester1_password"))
user_list.append(User("tester2_id", "tester2_name", "tester2_password"))
user_list.append(User("tester3_id", "tester3_name", "tester3_password"))

@bp.route("/", methods=["GET"])
def index():
    return redirect(url_for(f"{NAME}.login"))

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginFrom()

    if form.validate_on_submit():
        user_id = form.data.get("user_id")
        password = form.data.get("password")
        user = [user for user in user_list if user.user_id == user_id]
        if user:
            user = user[0]
            if user.password != password:
                flash("패스워드가 틀립니다.")
            else:
                session["user_id"] = user_id
                return redirect(url_for("base.index"))
        else:
            flash("유저가 존재하지 않습니다.")
    else:
        #error
        flash_form_errors(form)
    return render_template(f"{NAME}/login.html", form=form)

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterFrom()
    # form에는 method가 post인지 확인 할 수 있는 메서드가 존재한다.
    # 유효성이 통과 됐는지도 확인 할 수 있다.
    if form.validate_on_submit():
        user_id = form.data.get("user_id")
        user_name = form.data.get("user_name")
        password = form.data.get("password")
        user = [user for user in user_list if user.user_id == user_id]
        if user:
            flash("이미 존재하는 유저입니다.")
            # 기존의 페이지로 이동한다.
            return redirect(request.path)
        else:
            user_list.append(
                User(
                    user_id = user_id,
                    user_name = user_name,
                    password = password
                )
            )
            session["user_id"] = user_id
            return redirect(url_for("base.index"))
    else:
        #error
        flash_form_errors(form)
    return render_template(f"{NAME}/register.html", form=form)

@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for(f"{NAME}.login"))

def flash_form_errors(form):
    for _, errors in form.errors.items():
        for error in errors:
            flash(error)