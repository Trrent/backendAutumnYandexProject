from flask_restx import Resource, fields, Namespace
from src.items.services import get_item

api = Namespace('nodes', description='Базовые задачи')

item_fields = api.model('SystemItemImport', {
    'id': fields.String(title='Уникальный идентфикатор', required=True, nullable=False, example='элемент_1_4'),
    'url': fields.String(title='Ссылка на файл. Для папок поле равно null.', nullable=True, example='/file/url1'),
    'type': fields.String(title='Тип элемента - папка или файл', enum=['FOLDER', 'FILE'], required=True, example='FILE'),
    'parentId': fields.String(title='id родительской папки', nullable=True, example='элемент_1_1'),
    'size': fields.Integer(title='Целое число, для папок поле должно содержать null', nullable=True, example=234)
    })

item_list_fields = api.model('SystemItemImportRequest', {
    'items': fields.List(fields.Nested(item_fields)),
    'updateDate': fields.DateTime('Время обновления добавляемых элементов', nullable=False,
                                  example='2022-05-28T21:12:01.000Z')
})
error_fields = api.model('Error', {
    'code': fields.Integer(nullable=False, required=True),
    'message': fields.String(nullable=False, required=True)
})


@api.route('/<string:item_id>', strict_slashes=False)
class GetNode(Resource):
    @api.response(200, 'Информация об элементе', model=item_list_fields)
    @api.response(400, 'Невалидная схема документа или входные данные не верны.', model=error_fields)
    @api.response(404, 'Элемент не найден.', model=error_fields)
    def get(self, item_id):
        """
            Получить информацию об элементе по идентификатору. При получении информации о папке также предоставляется информация о её дочерних элементах.

            - для пустой папки поле children равно пустому массиву, а для файла равно null
            - размер папки - это суммарный размер всех её элементов. Если папка не содержит элементов, то размер равен 0. При обновлении размера элемента, суммарный размер папки, которая содержит этот элемент, тоже обновляется.
        """
        return get_item(item_id)


api.add_resource(GetNode)
