# googlekap앱에 모델을 연결 해주어야만 migrate등 db관련 작업을 할 수 있따.
from googlekap.models.memo import Memo as MemoModel
from flask_restx import Namespace

ns = Namespace("memos", description="메모 관련 api")
