from flask import Flask
import threading
from pyrogram import Client, idle
from flask import request
import json
import time
appTG = Client("my_account")
app = Flask(__name__)


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
        print("Mxx")
        m = appTG.get_chat_members_count(id)
        print("M:", m)
    except:
        print("MxxErr")
        err = m
        m = "Error"
    return m, err


@app.route('/')
def hello_world():
    appTG.send_message("me", "Hello from route")
    return 'Hello World!'


@app.route('/getchatmemberscount')
def get_num():
    chat_id = request.args.get('id')
    count, err = get_count(chat_id)
    if count == "Error":
        jsonStr = json.dumps({'count': 0, 'error': err})
    else:
        jsonStr = json.dumps({'count': count, 'error': None})

    return jsonStr, 200, {'Content-Type': 'application/json'}


@app.route('/getchatmembers')
def get_info():
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
    print("N:", n)
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
    print("slice len=", len(chatList))
    jsonStr = json.dumps(chatList)
    return jsonStr, 200, {'Content-Type': 'application/json'}


appTG.start()
threading.Thread(target=app.run, daemon=True).start()
idle()
appTG.stop()
