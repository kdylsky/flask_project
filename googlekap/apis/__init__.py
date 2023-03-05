from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint("api", __name__, url_prefix='/api')

api = Api(blueprint, title="Google Kap API", version='1.0', doc='/doc', description="Weloce my API docs")

# TODO: add namespace to Blueprint