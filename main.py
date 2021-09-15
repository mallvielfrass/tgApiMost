from flask import Flask
import threading
from pyrogram import Client, idle
from flask import request
import json
import time
from pyrogram.raw import functions
from pyrogram import types
from pyrogram import utils
from pyrogram.file_id import FileType
from pyrogram.scaffold import Scaffold

appTG = Client("my_account")
app = Flask(__name__)


def search_messages(id, user):
    m = None

    try:
        time.sleep(0.1)
        # print("id: ", id)
        z = appTG.search_messages(chat_id=id, from_user=user)
        # print(len(z))
        m = len(z)
        # m = {
        #     "id":  z.id,
        #     "is_self": z.is_self,
        #     "is_contact": z.is_contact,
        #     "is_mutual_contact": z.is_mutual_contact,
        #     "is_deleted": z.is_deleted,
        #     "is_bot": z.is_bot,
        #     "is_verified": z.is_verified,
        #     "is_restricted": z.is_restricted,
        #     "is_scam": z.is_scam,
        #     "is_fake": z.is_fake,
        #     "is_support": z.is_support,
        #     "first_name": z.first_name,
        #     "last_name": z.last_name,
        #     "status": z.status,
        #     "last_online_date": z.last_online_date,
        #     "next_offline_date": z.next_offline_date,
        #     "username": z.username,
        #     "language_code": z.language_code,
        #     "dc_id": z.dc_id,
        #     "phone_number": z.phone_number,
        #     "photo": z.photo.big_file_id,
        #     "restrictions": z.restrictions,
        #     "mention": z.mention,
        # }
    except Exception as e:
        print("e: ", e)
        return "Error", str(e)
    return m, None


def get_user(id):
    m = None

    try:
        time.sleep(0.1)
        # print("id: ", id)
        z = appTG.get_users(id)
        m = {
            "id":  z.id,
            "is_self": z.is_self,
            "is_contact": z.is_contact,
            "is_mutual_contact": z.is_mutual_contact,
            "is_deleted": z.is_deleted,
            "is_bot": z.is_bot,
            "is_verified": z.is_verified,
            "is_restricted": z.is_restricted,
            "is_scam": z.is_scam,
            "is_fake": z.is_fake,
            "is_support": z.is_support,
            "first_name": z.first_name,
            "last_name": z.last_name,
            "status": z.status,
            "last_online_date": z.last_online_date,
            "next_offline_date": z.next_offline_date,
            "username": z.username,
            "language_code": z.language_code,
            "dc_id": z.dc_id,
            "phone_number": z.phone_number,
            "photo": z.photo.big_file_id,
            "restrictions": z.restrictions,
            "mention": z.mention,
        }
    except Exception as e:
        print("e: ", e)
        return "Error", str(e)
    return m, None


def get_chats():
    z = []
    try:
        time.sleep(0.1)
        for dialog in appTG.iter_dialogs():
            z.append({
                "id": dialog.chat.id,
                "name": dialog.chat.title or dialog.chat.first_name,
                "type": dialog.chat.type,
                "membercount": dialog.chat.members_count or 0,

            })

    except:
        return "Error"
    return z


def check_chat_invite_link(id):
    m = None
    typeM = None
    try:
        time.sleep(0.1)
        print("id: ", id)
        z = appTG.get_chat(id)
        # x = appTG.send(
        #     functions.messages.CheckChatInvite(
        #         hash='t.me/joinchat/Ces3Vmef1Y1iOGNi'
        #     )
        # )
        # print("X in: ", type(z))
        tp = type(z)
        if tp == types.ChatPreview:
            # print("types.ChatPreview")
            typeM = "ChatPreview"
        elif tp == types.Chat:
            # print("types.Chat")
            typeM = "Chat"
        id = getattr(z, 'id', 0)

        m = {

            "id":  id,
            "typegroup": z.type,
            "title": z.title,
            "members_count": z.members_count,
            "typelink": typeM,
        }
        # for dialog in appTG.iter_dialogs():
        #     z.append({
        #         "id": dialog.chat.id,
        #         "name": dialog.chat.title or dialog.chat.first_name,
        #         "type": dialog.chat.type,
        #         "membercount": dialog.chat.members_count or 0,

        #     })

    except Exception as e:
        print("e: ", e)
        return "Error", str(e)
    return m, None


def get_member(chat_id, offset):
    err = ""
    try:
        time.sleep(0.1)
        m = appTG.get_chat_members(chat_id, offset=offset)
        z = []
        for item in m:
            z.append({
                "id": item["user"]["id"],
                "is_bot": item["user"]["is_bot"],
                "first_name": item["user"]["first_name"],
                "status": item["user"]["status"],
                "last_online_date": item["user"]["last_online_date"],
                "username": item["user"]["username"],
            })
        m = z
    except:
        print("error: ", m)
        err = m
        m = "Error"
    return m, err


def get_count(id):
    err = ""
    m = None
    try:
       # print("Mxx")
        m = appTG.get_chat_members_count(id)
       # print("M:", m)
    except:
        print("MxxErr")
        err = m
        m = "Error"
    return m, err


@app.route('/getuser')
def handle_get_user():
    id = request.args.get('id')
    user, err = get_user(id)
    if user == "Error":
        jsonStr = json.dumps({'user': None, 'error': err})
        return jsonStr, 200, {'Content-Type': 'application/json'}
    jsonStr = json.dumps({'user': user, 'error': err})
    return jsonStr, 200, {'Content-Type': 'application/json'}


@app.route('/search_messages')
def handle_search_messages():
    chat_id = request.args.get('chatid')
    user_id = request.args.get('userid')
    user, err = search_messages(chat_id, user_id)
    if user == "Error":
        jsonStr = json.dumps({'messages': None, 'error': err})
        return jsonStr, 200, {'Content-Type': 'application/json'}
    jsonStr = json.dumps({'messages': user, 'error': err})
    return jsonStr, 200, {'Content-Type': 'application/json'}


@app.route('/getchats')
def handle_get_chats():
    chats = get_chats()
    if chats == "Error":
        jsonStr = json.dumps({'chats': None, 'error': 'error get chats list'})
        return jsonStr, 200, {'Content-Type': 'application/json'}
    jsonStr = json.dumps({'chats': chats, 'error': None})

    return jsonStr, 200, {'Content-Type': 'application/json'}


@app.route('/getchatinvitelink')
def handle_get_chat_invite_link():
    chat_id = request.args.get('id')
    chats, e = check_chat_invite_link(chat_id)
    if chats == "Error":
        jsonStr = json.dumps({'info': None, 'error': e})
        return jsonStr, 200, {'Content-Type': 'application/json'}
    jsonStr = json.dumps({'info': chats, 'error': None})

    return jsonStr, 200, {'Content-Type': 'application/json'}


@app.route('/')
def handle_hello_world():
    appTG.send_message("me", "Hello from route")
    return 'Hello World!'


@app.route('/getchatmemberscount')
def handle_get_num():
    chat_id = request.args.get('id')
    count, err = get_count(chat_id)
    if count == "Error":
        jsonStr = json.dumps({'count': 0, 'error': err})
    else:
        jsonStr = json.dumps({'count': count, 'error': None})

    return jsonStr, 200, {'Content-Type': 'application/json'}


@app.route('/getchatmembers')
def handle_get_info():
    chat_id = request.args.get('id')
    count, err = get_count(chat_id)
    if count == "Error":
        jsonStr = json.dumps({'chatmember': None, 'error': err})
        return jsonStr, 200, {'Content-Type': 'application/json'}
    print(count)
    c = (count//200)+1
    n = c
    offset = 0
    chatList = []
    # print("N:", n)
    for i in range(1, n + 1):
      #  print("cicle:", i)
        zm, err = get_member(chat_id, offset)
        # chatList = get_chat_members()
        offset += 200
        if zm == "Error":
            # return "Error"
            print("off err")
            jsonStr = json.dumps({'chatmember': None, 'error': count})
            return jsonStr, 200, {'Content-Type': 'application/json'}
        else:
            chatList = [*chatList, *zm]
   # print("slice len=", len(chatList))
    jsonStr = json.dumps(chatList)
    return jsonStr, 200, {'Content-Type': 'application/json'}


appTG.start()
threading.Thread(target=app.run, daemon=True).start()
idle()
appTG.stop()
