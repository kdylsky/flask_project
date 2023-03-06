from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class LoginFrom(FlaskForm):
    # 프론트에 표시될 라벨과 유효성검사
    user_id = StringField("User Id", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterFrom(LoginFrom):
    user_name = StringField("User Name", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("repassword", message="Password mush match!!"),
        ],
    )
    repassword = PasswordField("RePassword", validators=[DataRequired()])
