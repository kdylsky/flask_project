from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request,
    g,
)
from googlekap.forms.auth_form import LoginFrom, RegisterFrom
from googlekap.models.user import User as UserModel
from werkzeug import security


NAME = "auth"
bp = Blueprint(NAME, __name__, url_prefix="/auth")


# before_request라면 blueprint에 해당하는 namespace에서만 동작하게 된다.
# before_app_request는 __init__에 연결한것과 비슷 동일하다.
@bp.before_app_request
def before_app_request():
    g.user = None
    user_id = session.get("user_id")

    if user_id:
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            g.user = user
        else:
            session.pop("user_id", None)


@bp.route("/", methods=["GET"])
def index():
    return redirect(url_for(f"{NAME}.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginFrom()

    if form.validate_on_submit():
        user_id = form.data.get("user_id")
        password = form.data.get("password")
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            if not security.check_password_hash(user.password, password):
                flash("패스워드가 틀립니다.")
            else:
                session["user_id"] = user.user_id
                return redirect(url_for("base.index"))
        else:
            flash("유저가 존재하지 않습니다.")
    else:
        # error
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
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            flash("이미 존재하는 유저입니다.")
            # 기존의 페이지로 이동한다.
            return redirect(request.path)
        else:
            user = UserModel(
                user_id=user_id,
                user_name=user_name,
                password=security.generate_password_hash(password),
            )
            g.db.add(user)
            g.db.commit()
            session["user_id"] = user_id
            return redirect(url_for("base.index"))
    else:
        # error
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
