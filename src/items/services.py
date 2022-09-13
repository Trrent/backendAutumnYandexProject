from src.items.models import ItemModel, HistoryModel
from src.items.schemas import item_schema, history_schema, item_list_schema
from datetime import datetime


def create_item(data):
    """Выдает сериализованные данные, десериализует их и создает новый элемент"""
    items, date = data['items'], data['updateDate']
    if check_request_data(items, date):

        from marshmallow import ValidationError

        valid_items = []
        try:
            for item in items:
                item['date'] = date
                valid_item = item_schema.load(item)
                valid_item.parentId = item.get('parentId', None)
                valid_item.size = item.get('size', 0)
                valid_items.append(valid_item)
        except ValidationError as error:
            print(error)
            return {"code": 400, "message": "Validation Failed"}, 400
        else:
            for item in valid_items:
                item.save()
            return {'code': 200, 'message': 'Вставка или обновление прошли успешно.'}, 200
    return {"code": 400, "message": "Validation Failed"}, 400


def get_item(item_id):
    """Получить элемент по id"""
    item = ItemModel.find_by_id(item_id)
    if item:
        item_data = item.json()
        return item_data, 200
    return {"code": 404, "message": "Item not found"}, 404


def delete_item(date, item_id):
    """Удалить элемент по id"""
    item = ItemModel.find_by_id(item_id)
    if item:
        if not validate_iso8601(date):
            return {"code": 400, "message": "Validation Failed"}, 400
        item.date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        item.delete()
        return {'code': 200, 'message': 'Удаление прошло успешно.'}, 200
    return {"code": 404, "message": "Item not found"}, 404


def update_history(date):
    """Получть список файлов, обновленных за последние 24 часа от date"""
    if not validate_iso8601(date):
        return {"code": 400, "message": "Validation Failed"}, 400
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    response = {'items': []}
    for item in HistoryModel.find_last_updates(date):
        response['items'].append(item.json())
    return response, 200


def node_history(item_id, date_start, date_end):
    """Получение истории обновлений по элементу за заданный полуинтервал [date_start, date_end)."""
    item = ItemModel.find_by_id(item_id)
    if item:
        if not validate_iso8601(date_start) and not validate_iso8601(date_end):
            return {"code": 400, "message": "Validation Failed"}, 400
        date_start = datetime.strptime(date_start, "%Y-%m-%dT%H:%M:%SZ")
        date_end = datetime.strptime(date_end, "%Y-%m-%dT%H:%M:%SZ")
        response = {'items': []}
        for item in HistoryModel.find_node_history(item_id, date_start, date_end):
            response['items'].append(item.json())
        return response, 200
    return {"code": 404, "message": "Item not found"}, 404


def validate_iso8601(line):
    """Проверка строки line с датой на валидность"""
    try:
        datetime.strptime(line, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return False
    return True


def check_request_data(items, date):
    if any(i['id'] is None if i.get('id') else True for i in items):
        return False
    if not all(ItemModel.find_by_id(i['parentId']).type == 'FOLDER' for i in filter(lambda x: x.get('parenId') is not None, items)):
        return False
    if not all(i.get('url') is None if i['type'] == 'FOLDER' else True for i in items):
        return False
    if not all(True if i.get('url') else False for i in filter(lambda x: x['type'] == 'FILE', items)):
        return False
    if not all(len(i['url']) <= 255 if i['type'] == 'FILE' and isinstance(i['url'], str) else True for i in items):
        return False
    if not all(i.get('size') is None if i['type'] == 'FOLDER' else True for i in items):
        return False
    if not all(i.get('size') and isinstance(i.get('size'), int) for i in filter(lambda x: x['type'] == 'FILE', items)):
        return False
    if not all(i['size'] > 0 if i['type'] == 'FILE' else True for i in filter(lambda x: x.get('size') is not None, items)):
        return False
    items_id = [i['id'] for i in items]
    if any(items_id.count(i['id']) > 1 for i in items):
        return False
    if not validate_iso8601(date):
        return False
    print(4)
    if any(i['type'] not in ['FOLDER', 'FILE'] for i in items):
        return False
    if any(i['id'] == i.get('parentId', '') for i in items):
        return False
    return True



