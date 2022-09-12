from datetime import datetime

from src import db
from typing import List


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.String, primary_key=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String, nullable=False)
    parentId = db.Column(db.String, db.ForeignKey('items.id'), nullable=True)
    size = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime)

    children = db.relationship('ItemModel', cascade="all,delete", backref=db.backref('parent', remote_side=id),
                               remote_side=parentId)

    def __init__(self, id, date, type, url=None, parentId=None, size=None):
        self.date = date
        self.size = size
        self.parentId = parentId
        self.type = type
        self.url = url
        self.id = id

    def json(self):
        size = self.get_item_size()
        isodate = f"{self.date.isoformat()}Z"
        return {
            'date': isodate,
            'size': size,
            'parentId': self.parentId,
            'type': self.type,
            'url': self.url,
            'id': self.id,
            'children': self.get_children_list()
        }

    def __repr__(self):
        return f"ItemModel(id={self.id}, type={self.type})"

    @classmethod
    def find_by_id(cls, _id) -> "ItemModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def get_children_list(self) -> ["dict"]:
        children_list = []
        if self.children:
            for child in self.children:
                children_list.append(child.json())
            return children_list
        return None

    def get_item_size(self) -> "int":
        size = self.size
        if self.children:
            for child in self.children:
                size += child.get_item_size()
        return size

    def save(self) -> None:
        log = HistoryModel(self.id, self.date, self.type, self.url, self.parentId, self.get_item_size())
        db.session.add(self)
        db.session.add(log)
        db.session.commit()
        if self.parent:
            self.parent.date = self.date
            self.parent.save()

    def delete(self) -> None:
        parent = self.parent
        if parent:
            parent.date = self.date
        log = HistoryModel(self.id, self.date, self.type, self.url, self.parentId, self.get_item_size())
        db.session.delete(self)
        db.session.add(log)
        db.session.commit()
        if parent:
            parent.save()


class HistoryModel(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.String, db.ForeignKey('items.id'), nullable=False)
    url = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=False)
    parentId = db.Column(db.String, db.ForeignKey('items.id'), nullable=True)
    size = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime)

    def __init__(self, id, date, type, url=None, parentId=None, size=None):
        self.date = date
        self.isodate = f"{self.date.isoformat()}.{str(self.date.microsecond)}Z"
        self.size = size
        self.parentId = parentId
        self.type = type
        self.url = url
        self.item_id = id

    def __repr__(self):
        return f"HistoryModel(id={self.id}, item_id={self.item_id}, type={self.type})"

    @classmethod
    def find_by_item_id(cls, _item_id) -> ["HistoryModel"]:
        return cls.query.filter_by(item_id=_item_id).all()

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

