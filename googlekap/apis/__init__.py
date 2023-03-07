from flask import Blueprint, g, abort, current_app
from flask_restx import Api
from .user import ns as UserNamespace
from .memo import ns as MemoNamespace
from functools import wraps

blueprint = Blueprint("api", __name__, url_prefix="/api")


# 데코레이터
# 함수를 인자로 받는다. 인자로 받은 함수를 func 실행시켜준다.
# 실행시켜준 함수를 리턴한다.
def check_session(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        if not g.user:
            abort(401)
        return func(*args, **kwargs)

    return __wrapper


api = Api(
    blueprint,
    title="Google Kap API",
    version="1.0",
    doc="/doc",
    decorators=[check_session],
    description="Weloce my API docs",
)

# TODO: add namespace to Blueprint
api.add_namespace(UserNamespace)
api.add_namespace(MemoNamespace)
