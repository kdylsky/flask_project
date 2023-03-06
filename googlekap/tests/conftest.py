# 모듈 별로 fixture를 관리하기 용이하게 끔 디렉토리 안에 공통적으로 이용할 수 있는 코드이다.
import sys

sys.path.append(".")

from googlekap.configs import TestingConfig
from googlekap import create_app, db
from googlekap.models.user import User as UserModel
import pytest


# 더미 유저 데이터 만들기
@pytest.fixture
def user_data():
    yield dict(user_id="test_id", user_name="test_name", password="test_password")


@pytest.fixture()
def app(user_data):
    app = create_app(TestingConfig)
    # 이 컨텍스트 안에서 데이터베이스 초기화
    with app.app_context():
        db.drop_all()
        db.create_all()  # flask db가 업그레이드 된 것 처럼 동작한다.
        db.session.add(UserModel(**user_data))
        db.session.commit()
    yield app


# pytest -sv => pytest
# ptw => pytest-watch
@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
