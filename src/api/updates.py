from flask_restx import Resource, fields, Namespace, reqparse
from src.items.services import update_history

api = Namespace('updates', description='Дополнительные задачи')

item_fields = api.model('SystemItemHistoryUnit', {
    'id': fields.String(title='Уникальный идентфикатор', required=True, nullable=False, example='элемент_1_4'),
    'url': fields.String(title='Ссылка на файл. Для папок поле равно null.', nullable=True, example='/file/url1'),
    'type': fields.String(title='Тип элемента - папка или файл', enum=['FOLDER', 'FILE'], required=True, example='FILE'),
    'parentId': fields.String(title='id родительской папки', nullable=True, example='элемент_1_1'),
    'size': fields.Integer(title='Целое число, для папок поле должно содержать null', nullable=True, example=234),
    'date': fields.DateTime(title='Время последнего обновления элемента.', required=True, nullable=False, example='2022-05-28T21:12:01.000Z')
    })

item_list_fields = api.model('SystemItemHistoryResponse', {
    'items': fields.List(fields.Nested(item_fields))
})


error_fields = api.model('Error', {
    'code': fields.Integer(nullable=False, required=True),
    'message': fields.String(nullable=False, required=True)
})

parser = reqparse.RequestParser()
parser.add_argument('date', type=str)


@api.route('/', strict_slashes=False)
@api.param('date', description='Дата и время запроса', example='2022-05-28T21:12:01.516Z', required=True)
class GetNodesHistory(Resource):
    @api.response(200, 'Информация об элементе', model=item_list_fields)
    @api.response(400, 'Невалидная схема документа или входные данные не верны.', model=error_fields)
    def get(self):
        """
            Получение списка файлов, которые были обновлены за последние 24 часа включительно [date - 24h, date] от времени переданном в запросе.
        """
        args = parser.parse_args()
        date = args['date']
        return update_history(date)


api.add_resource(GetNodesHistory)
