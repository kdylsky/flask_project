# 모듈 별로 fixture를 관리하기 용이하게 끔 디렉토리 안에 공통적으로 이용할 수 있는 코드이다.
import sys

sys.path.append(".")

from googlekap.configs import TestingConfig
from googlekap import create_app, db
from googlekap.models.user import User as UserModel
from googlekap.models.memo import Memo as MemoModel
import pytest
import os


# 더미 유저 데이터 만들기
@pytest.fixture(scope="session")
def user_data():
    yield dict(
        user_id="test_id",
        user_name="test_name",
        password="test_password",
    )


# 더미 데이터 메모 만들기
@pytest.fixture(scope="session")
def memo_data():
    yield dict(
        title="tite",
        content="content",
    )


@pytest.fixture(scope="session")
def app(user_data, memo_data):
    app = create_app(TestingConfig)
    # 이 컨텍스트 안에서 데이터베이스 초기화
    with app.app_context():
        db.drop_all()
        db.create_all()  # flask db가 업그레이드 된 것 처럼 동작한다.
        user = UserModel(**user_data)
        db.session.add(user)
        # db에 commit하는 것 처럼 flush를 해주어야지만 user.id를 받아올 수 있다.
        db.session.flush()
        memo_data["user_id"] = user.id
        db.session.add(MemoModel(**memo_data))
        db.session.commit()
        yield app
        # 불필요한 디비 정리
        db.drop_all()
        db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
        if db_path:
            os.remove(db_path)


# pytest -sv => pytest
# ptw => pytest-watch
@pytest.fixture(scope="session")
def client(app, user_data):
    with app.test_client() as client:
        # NOTE: 세션 입혀주기
        # auth_router에 before_app_reqeust에서 session에 user_id를 넣어준다.
        # 테스트에서도 아래와 같이 client에 session을 추가해주어야 문제가 발생하지 않는다.
        with client.session_transaction() as session:
            session["user_id"] = user_data.get("user_id")
        yield client
