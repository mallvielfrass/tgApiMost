from pyrogram import Client
from flask import Flask
from flask import request
import time
import multiprocessing
import json

appX = Flask(__name__)

timeOut = 0


@appX.route('/getlatesttime')
def get_timestamp():
    return str(timeOut)


def get_member(queue, chat_id, offset):
    with Client("my_account") as app:
        try:

            m = app.get_chat_members(chat_id, offset=offset)
            z = []
    # m = app.get_chat_members("@Manehattan", limit=5, offset=0)
    # print(m[0])
            for item in m:
                z.append({
                    "id": item["user"]["id"],
                    "is_bot": item["user"]["is_bot"],
                    "first_name": item["user"]["first_name"],
                    "status": item["user"]["status"],
                    "last_online_date": item["user"]["last_online_date"],
                    "username": item["user"]["username"],
                })
            # print(z)
           # for item in m:
           #     print("item+++===", item["pyrogram.types.ChatMember"])
           #     z.append(item["pyrogram.types.ChatMember"])

           #     print("ZZZZZZZ++===", z)
            m = z
        except:
            print("error: ", m)
            m = "Error"
        # print("MMM: ", z)
        # print("m:: "+str(len(z))+" return off:", str(offset))
        # time.sleep(10)
        queue.put(m)


def inf(queue, chat_id):
    with Client("my_account") as app:
        try:
            m = app.get_chat_members_count(chat_id)
        except:
            m = "Error"
        queue.put(m)

# http://127.0.0.1:5000/getchatmemberscount?id=-1001192016123


@appX.route('/getchatmemberscount')
def get_num():
    chat_id = request.args.get('id')

    global timeOut
    timeLocal = time.time()
    if timeLocal < timeOut+3:
        return "error"
    else:
        timeOut = timeLocal

    print("debug point")
    m_count = 0

    queue = multiprocessing.Queue()

    p = multiprocessing.Process(target=inf, args=(queue, chat_id,))
    p.start()
    p.join()
    m = queue.get()
    if m == "Error":
        return "error"

    jsonStr = json.dumps({'count': str(m)})

    return jsonStr, 200, {'Content-Type': 'application/json'}

# http://127.0.0.1:5000/getchatmembers?id=-1001192016123


@appX.route('/getchatmembers')
def get_info():
    chat_id = request.args.get('id')

    global timeOut
    timeLocal = time.time()
    if timeLocal < timeOut+3:
        return "error"
    else:
        timeOut = timeLocal
    # if timeLocal
    m_count = 0

    queue = multiprocessing.Queue()

    p = multiprocessing.Process(target=inf, args=(queue, chat_id,))
    p.start()
    p.join()
    m = queue.get()
    if m == "Error":
        return "Error"

    # _count = ()
# "@Manehattan"
    print(" m :",  m)

    try:
        m = int(m)
    except ValueError:
        # Handle the exception
        print('Please enter an integer M')
        return 'Please enter an integer M'
    c = (m//200)+1
    sum = 0

    n = c
    offset = 0
    chatList = []
    print("N:", n)
    for i in range(1, n + 1):
        print("cicle:", i)
       # chatList = get_chat_members()
        queueZ = multiprocessing.Queue()
        p = multiprocessing.Process(
            target=get_member, args=(queueZ, chat_id, offset,))
        p.start()
        # p.join()
        zm = queueZ.get()
        offset += 200
        if zm == "Error":
            # return "Error"
            print("off err")
        else:
            print("zm:")
            chatList = [*chatList, *zm]
            time.sleep(0.3)
    print("slice len=", len(chatList))
    jsonStr = json.dumps(chatList)

    return jsonStr, 200, {'Content-Type': 'application/json'}


def main():
    print(">run server")

    appX.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == "__main__":
    main()
