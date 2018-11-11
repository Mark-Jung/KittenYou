import os

from db import db
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, send, emit

from util.parser import ReqParser

from controller.MessageController import MessageController

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///localdata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
"""
till here
"""

if __name__ == '__main__':
    CORS(app)

@app.route('/hi')
def hello_world():
    return "running!"

@socketio.on('new_message')
def make_new_message(data):
    req_params = ["username", "room", "message"]
    if not ReqParser.check_body(data, req_params):
        emit('error', {"error_message": 'invalid params'}, json=True)
    username = data['username']
    room = data['room']
    message = data['message']
    new_message = MessageController.clean_message(username, room, message)
    emit("new_message", new_message, room=room)

@socketio.on('join')
def on_join(data):
    req_params = ["username", "room"]
    if not ReqParser.check_body(data, req_params):
        emit('error', {"error_message": 'invalid params'}, json=True)
    username = data['username']
    room = data['room']
    join_room(room)
    old_messages = MessageController.get_old_messages(room)
    emit("joined_room", old_messages)
    joined_notify = MessageController.new_message("Admin", room, username + " has entered the room.")
    emit("new_message", joined_notify, room=room)

@socketio.on('leave')
def on_leave(data):
    req_params = ["username", "room"]
    if not ReqParser.check_body(data, req_params):
        emit('error', {"error_message": 'invalid params'}, json=True)
    username = data['username']
    room = data['room']
    leave_room(room)
    emit("new_message", username + ' has left the room.', room=room)

if __name__ == '__main__':
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    socketio.run(app)
