from flask_restx import Resource, fields, Namespace, reqparse
from src.items.services import node_history

api = Namespace('node', description='Дополнительные задачи')

item_fields = api.model('SystemItemHistoryUnit', {
    'id': fields.String(title='Уникальный идентфикатор', required=True, nullable=False, example='элемент_1_4'),
    'url': fields.String(title='Ссылка на файл. Для папок поле равно null.', nullable=True, example='/file/url1'),
    'type': fields.String(title='Тип элемента - папка или файл', enum=['FOLDER', 'FILE'], required=True,
                          example='FILE'),
    'parentId': fields.String(title='id родительской папки', nullable=True, example='элемент_1_1'),
    'size': fields.Integer(title='Целое число, для папок поле должно содержать null', nullable=True, example=234),
    'date': fields.DateTime(title='Время последнего обновления элемента.', required=True, nullable=False,
                            example='2022-05-28T21:12:01Z')
})

item_list_fields = api.model('SystemItemHistoryResponse', {
    'items': fields.List(fields.Nested(item_fields))
})

error_fields = api.model('Error', {
    'code': fields.Integer(nullable=False, required=True),
    'message': fields.String(nullable=False, required=True)
})

parser = reqparse.RequestParser()
parser.add_argument('dateStart', type=str)
parser.add_argument('dateEnd', type=str)


@api.route('/<string:item_id>/history', strict_slashes=False)
@api.param('dateStart',
           description='Дата и время начала интервала, для которого считается история. Дата должна обрабатываться согласно ISO 8601 (такой придерживается OpenAPI). Если дата не удовлетворяет данному формату, необходимо отвечать 400.',
           example='2022-05-28T21:12:01Z')
@api.param('dateEnd',
           description='Дата и время конца интервала, для которого считается история. Дата должна обрабатываться согласно ISO 8601 (такой придерживается OpenAPI). Если дата не удовлетворяет данному формату, необходимо отвечать 400.',
           example='2022-05-28T21:12:01Z')
class GetNodeHistory(Resource):
    @api.response(200, 'Информация об элементе', model=item_list_fields)
    @api.response(400, 'Невалидная схема документа или входные данные не верны.', model=error_fields)
    @api.response(404, 'Элемент не найден.', model=error_fields)
    def get(self, item_id):
        """
            Получение истории обновлений по элементу за заданный полуинтервал [from, to). История по удаленным элементам недоступна.

            - размер папки - это суммарный размер всех её элементов
            - можно получить статистику за всё время.
        """
        args = parser.parse_args()
        date_start = args.get('dateStart')
        date_end = args.get('dateEnd')
        return node_history(item_id, date_start, date_end)


api.add_resource(GetNodeHistory)
