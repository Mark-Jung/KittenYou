from db import db
from datetime import datetime

from model.basemodel import BaseModel
from util.jsonable import JsonEncodedDict

class MessageModel(db.Model, BaseModel):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    writer = db.Column(db.String(255))
    room = db.Column(db.String(255))
    message = db.Column(db.String(10000))


    def __init__(self, writer, room, message):
        self.writer = writer
        self.room = room
        self.message = message
        self.date_created = datetime.now()

    def json(self):
        return {
                "id": self.id,
                "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "room": self.room,
                "message": self.message,
                "writer": self.writer,
                }

    @classmethod
    def filter_by_room(cls, room):
        return cls.query.filter_by(room=room).all()
