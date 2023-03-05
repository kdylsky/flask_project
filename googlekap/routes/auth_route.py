from flask import Blueprint, render_template
from googlekap.forms.auth_form import LoginFrom, RegisterFrom

NAME = "auth"
bp = Blueprint(NAME, __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user_id = form.data.get("user_id")
        password = form.data.get("password")
        print(user_id, password)
    else:
        #error
        pass
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
        repassword = form.data.get("repassword")
        print(user_id, user_name, password, repassword)
    else:
        #error
        pass
    return render_template(f"{NAME}/register.html", form=form)

@bp.route("/logout")
def logout():
    return "logout"

