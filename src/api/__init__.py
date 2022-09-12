from flask import Blueprint
from flask_restx import Api

from src.api.imports import api as imports_ns
from src.api.nodes import api as node_ns
from src.api.delete import api as delete_ns
from src.api.updates import api as updates_ns

api_bp = Blueprint('api', __name__)
api = Api(api_bp, title='Yet Another Disk',
          description='Вступительное задание в Осеннюю Школу Бэкенд Разработки Яндекса 2022')

api.add_namespace(imports_ns)
api.add_namespace(node_ns)
api.add_namespace(delete_ns)
api.add_namespace(updates_ns)
