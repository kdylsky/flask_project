# googlekap앱에 모델을 연결 해주어야만 migrate등 db관련 작업을 할 수 있따.
from googlekap.models.memo import Memo as MemoModel

# memo에 있는 유저데이터에 join하기 위해서 유저 모델이 필요하다.
from googlekap.models.user import User as UserModel

from flask_restx import Namespace, fields, Resource, reqparse
from flask import g, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import shutil

ns = Namespace("memos", description="메모 관련 api")

memo = ns.model(
    "Memo",
    {
        "id": fields.Integer(required=True, description="메모 고유 아이디"),
        "user_id": fields.Integer(required=True, description="메모 유저 아이디"),
        "title": fields.String(required=True, description="메모 타이틀"),
        "linked_image": fields.String(required=False, description="메모 이미지 경로"),
        "content": fields.String(required=True, description="메모 내용"),
        "created_at": fields.DateTime(description="메모 생성 작성일"),
        "updated_at": fields.DateTime(description="메모 변경일"),
    },
)

post_parser = reqparse.RequestParser()
post_parser.add_argument("title", required=True, help="메모 타이틀")
post_parser.add_argument("content", required=True, help="메모 내용")
post_parser.add_argument(
    "linked_image", location="files", required=False, type=FileStorage, help="메모 이미지"
)

put_parser = post_parser.copy()
put_parser.replace_argument("title", required=False, help="메모 수정 타이틀")
put_parser.replace_argument("content", required=False, help="메모 수정 내용")

get_parser = reqparse.RequestParser()
get_parser.add_argument("page", required=False, type=int, help="메모 페이지 번호")
get_parser.add_argument("needle", required=False, help="메모 검색어")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "gif",
    }


def randomword(length):
    import random, string

    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def save_file(file):
    if file.filename == "":
        ns.abort(400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        relateive_path = os.path.join(
            current_app.static_url_path[1:],  # /static -> static
            current_app.config["USER_STATIC_BASE_DIR"],  # static/user_images
            g.user.user_id,  # static/user_images/{user_id}
            "memos",  # static/user_images/{user_id}/memos
            randomword(5),  # static/user_images/{user_id}/asdfs
            filename,  # static/user_images/{user_id}/asdfs/{filename}
        )

        upload_path = os.path.join(current_app.root_path, relateive_path)

        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        return relateive_path, upload_path
    else:
        ns.abort(400)


@ns.route("")
class MemoList(Resource):
    @ns.marshal_list_with(memo, skip_none=True)
    @ns.expect(get_parser)
    def get(self):
        """메모 복수 조회"""
        args = get_parser.parse_args()
        page = args["page"]
        needle = args["needle"]

        per_page = 5
        basic_query = MemoModel.query.join(
            UserModel,
            UserModel.id == MemoModel.user_id,
        ).filter(UserModel.id == g.user.id)

        if needle:
            needle = f"%{needle}%"
            basic_query = basic_query.filter(
                MemoModel.title.ilike(needle) | MemoModel.content.ilike(needle)
            )

        pages = basic_query.order_by(MemoModel.created_at.desc()).paginate(
            page=page, per_page=per_page
        )
        print(pages)
        return pages.items

    @ns.marshal_list_with(memo, skip_none=True)
    @ns.expect(post_parser)
    def post(self):
        """메모 생성"""
        args = post_parser.parse_args()
        memo = MemoModel(
            title=args["title"], content=args["content"], user_id=g.user.id
        )
        file = args["linked_image"]
        if file:
            relateive_path, _ = save_file(file)
            memo.linked_image = relateive_path
        g.db.add(memo)
        g.db.commit()
        return memo, 201


@ns.param("id", "메모 고유 아이디")
@ns.route("/<int:id>")
class Memo(Resource):
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self, id):
        """메모 단수 조회"""
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        return memo

    @ns.marshal_list_with(memo, skip_none=True)
    @ns.expect(put_parser)
    def put(self, id):
        """메모 수정"""
        args = put_parser.parse_args()
        memo = MemoModel.query.get_or_404(id)

        if g.user.id != memo.user_id:
            ns.abort(403)
        if args["title"] is not None:
            memo.title = args["title"]
        if args["content"] is not None:
            memo.content = args["content"]
        file = args["linked_image"]
        if file:
            relateive_path, upload_path = save_file(file)
            if memo.linked_image:
                origin_path = os.path.join(current_app.root_path, memo.linked_image)
                if origin_path != upload_path:
                    if os.path.isfile(origin_path):
                        shutil.rmtree(os.path.dirname(origin_path))
            memo.linked_image = relateive_path

        g.db.commit()
        return memo

    def delete(self, id):
        """메모 삭제"""
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        g.db.delete(memo)
        g.db.commit()
        return "", 204


@ns.param("id", "메모 고유 아이디")
@ns.route("/<int:id>/image")
class MemoImage(Resource):
    def delete(self, id):
        """메모 이미지 삭제"""
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        if memo.linked_image:
            origin_path = os.path.join(
                current_app.root_path,
                memo.linked_image,
            )
            if os.path.isfile(origin_path):
                shutil.rmtree(os.path.dirname(origin_path))
            memo.linked_image = None
            g.db.commit()
        return "", 204
