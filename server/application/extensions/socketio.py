from application.server import sio

users = []
def add_user(socketId, userId):
    if userId not in users:
        users.append({"socketId": socketId, "userId": userId})

def remove_user(socketId):
    for user in users:
        if user["socketId"] == socketId:
            users.remove(user)

@sio.event
async def setup(sid, user_id):
    if user_id is not None:
        sio.enter_room(sid, user_id)
        add_user(sid, user_id)
        await sio.emit("get_users", data=users)

@sio.event
async def disconnect(sid):
    remove_user(sid)
    await sio.emit("get_users", data=users)


@sio.event
async def new_message(sid, newMessageRecieved):
    message = newMessageRecieved["message"]
    for user in users:
        if user["userId"] != message["sender_id"]:
            await sio.emit("message_received", data=newMessageRecieved, room=user["socketId"]) 

@sio.event
async def entering(sid, data):
    for user in users:
        if user["userId"] == data["userId"]:
            await sio.emit("entering", data=data["chatId"], room=data["userId"])