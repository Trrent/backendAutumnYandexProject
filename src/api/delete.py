from flask import request
from flask_restx import Resource, fields, Namespace, reqparse, marshal_with
from src.items.services import delete_item

api = Namespace('delete', description='Базовые задачи')

error_fields = api.model('Error', {
    'code': fields.Integer(nullable=False, required=True),
    'message': fields.String(nullable=False, required=True)
})

parser = reqparse.RequestParser()
parser.add_argument('date', type=str)


@api.route('/<string:item_id>', strict_slashes=False)
@api.param('date', description='Дата и время запроса', example='2022-05-28T21:12:01Z', required=True)
@api.param('item_id', description='Идентификатор', example='элемент_1_1')
class DeleteNode(Resource):
    @api.response(200, 'Удаление прошло успешно.')
    @api.response(400, 'Невалидная схема документа или входные данные не верны.', model=error_fields)
    @api.response(404, 'Элемент не найден.', model=error_fields)
    def delete(self, item_id):
        """
            Удалить элемент по идентификатору. При удалении папки удаляются все дочерние элементы. Доступ к истории обновлений удаленного элемента невозможен.

            **Обратите, пожалуйста, внимание на этот обработчик. При его некорректной работе тестирование может быть невозможно.**
        """
        args = parser.parse_args()
        date = args['date']
        return delete_item(date, item_id)


api.add_resource(DeleteNode)
