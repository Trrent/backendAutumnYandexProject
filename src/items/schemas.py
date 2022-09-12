from src import ma
from src.items.models import ItemModel, HistoryModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True
        include_fk = True


class HistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistoryModel
        load_instance = True
        include_fk = True


item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

history_schema = HistorySchema()
history_list_schema = HistorySchema(many=True)