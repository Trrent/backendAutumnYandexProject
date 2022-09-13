from flask import request
from flask_restx import Resource, fields, Namespace
from src.items.services import create_item

api = Namespace('imports', description='Базовые задачи')


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
                                  example='2022-05-28T21:12:01Z')
})

error_fields = api.model('Error', {
    'code': fields.Integer(nullable=False, required=True),
    'message': fields.String(nullable=False, required=True)
})


@api.route('/', strict_slashes=False)
class AddNodes(Resource):
    @api.expect(item_list_fields)
    @api.response(200, 'Вставка или обновление прошли успешно.')
    @api.response(400, 'Невалидная схема документа или входные данные не верны.', model=error_fields)
    def post(self):
        """
            Импортирует элементы файловой системы. Элементы импортированные повторно обновляют текущие.
            Изменение типа элемента с папки на файл и с файла на папку не допускается.
            Порядок элементов в запросе является произвольным.

              - id каждого элемента является уникальным среди остальных элементов
              - поле id не может быть равно null
              - родителем элемента может быть только папка
              - принадлежность к папке определяется полем parentId
              - элементы могут не иметь родителя (при обновлении parentId на null элемент остается без родителя)
              - поле url при импорте папки всегда должно быть равно null
              - размер поля url при импорте файла всегда должен быть меньше либо равным 255
              - поле size при импорте папки всегда должно быть равно null
              - поле size для файлов всегда должно быть больше 0
              - при обновлении элемента обновленными считаются **все** их параметры
              - при обновлении параметров элемента обязательно обновляется поле **date** в соответствии с временем обновления
              - в одном запросе не может быть двух элементов с одинаковым id
              - дата обрабатывается согласно ISO 8601 (такой придерживается OpenAPI). Если дата не удовлетворяет данному формату, ответом будет код 400.

            Гарантируется, что во входных данных нет циклических зависимостей и поле updateDate монотонно возрастает. Гарантируется, что при проверке передаваемое время кратно секундам.
        """
        return create_item(request.get_json())


api.add_resource(AddNodes)
