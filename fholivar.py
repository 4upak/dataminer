import json
from os import walk
from models.autoria_item import Autoria_item, Phone, Car
from models.telegram_account import Telegram_account
from telethon import TelegramClient, sync
from models.proxy import Proxy
from models.task import Task
from models.telegram_account_groups import Telegram_account_groups
from telethon import events
from telethon import functions, types
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, PeerUser, PeerChat, PeerChannel, User, Channel, Chat
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from database import Base,session,engine
import socks
import asyncio
import re
import time
from models.autoria_item import Autoria_item
from models.phone import Phone
from models.dialog import Telegram_dialog
import random
import time
from datetime import datetime
from database import Base,session,engine
from telethon import functions, types
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from os import walk

def get_account_from_db_holivar():
    try:
        result =  session.query(Telegram_account).filter(Telegram_account.deleted==0).filter(Telegram_account.message_restricted==0).filter(Telegram_account.online==0).filter(Telegram_account.action=='-').first()
        session.query(Telegram_account).filter(Telegram_account.telegram_id == result.telegram_id).update({'work': 2})
        session.commit()


    except Exception as ex:
        print(ex)
        return False

    return result
def get_reply(text,me):
    from models.holivar import Holivar_unit
    count = session.query(Holivar_unit).filter(Holivar_unit.message == text).count()
    if count>0:
        print("Пришел холиварный ответ")
        res = session.query(Holivar_unit).filter(Holivar_unit.message == text).first()
        key = res.key
        ans_count = session.query(Holivar_unit).filter(Holivar_unit.answer_to_key == key).filter(Holivar_unit.user_id == me.id).count()
        if ans_count>0:
            print("Нужно отвеачать")
            res = session.query(Holivar_unit).filter(Holivar_unit.answer_to_key == key).filter(Holivar_unit.user_id == me.id).first()
            print (f"Текст ответа: {res.message}")
            return res.message
    else:
        return False

def check_restriction(me,ex):
    if re.search('Too many requests', str(ex)) or re.search("banned from sending messages", str(ex)):
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'restricted': 1, 'message_restricted': 1})
        session.commit()
    if re.search("deleted/deactivated", str(ex)):
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'deleted': 1})
        session.commit()

    if re.search("joined too many channels", str(ex)):
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'restricted': 1, 'invite_restricted': 1})
        session.commit()

    if re.search("joined too many channels", str(ex)):
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'restricted': 1, 'invite_restricted': 1})
        session.commit()

    if re.search("seconds is required", str(ex)):
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'restricted': 1, 'invite_restricted': 1})
        session.commit()

    if re.search("have joined too many channels", str(ex)):
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'restricted': 1})
        session.commit()

    if re.search("banned from sending messages in supergroups/channels", str(ex)):
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'restricted': 1, 'message_restricted': 1})
        session.commit()

    return True

async def holivar_controller(client,me):

    session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update({'action': 'holivar', 'work': 2})
    session.commit()
    count = 0
    tasks = session.query(Task).filter(Task.sender_id == me.username).filter(Task.done == 0).all()
    print(f"Колическо заданий в базе:{len(tasks)}")
    invite_count = 0

    f = open("fio.txt", "r")
    lines = f.readlines()
    f.close()
    fio = lines[random.randrange(0, len(lines) - 1)]
    name = fio.split(' ')[1]
    lastname = fio.split(' ')[0]

    #change_name
    try:
        await client(UpdateProfileRequest(first_name=name, last_name=lastname))
        print(f"аккаунт изменил имя на:{name} {lastname}")

    except Exception as ex:
        print(ex)
        print("Имя изменить не смогли")

    await asyncio.sleep(10)

    # change_avatar
    try:
        avatars = []
        for (dirpath, dirnames, filenames) in walk('avatars'):
            for file in filenames:
                avatars.append(file)
        new_avatar = avatars[random.randrange(0, len(avatars) - 1)]
        file_name = f"/Users/sergeychupak/PycharmProjects/dataminer/avatars/{new_avatar}"
        print(file_name)
        print("Загружаем файл")
        file = await client.upload_file(file_name)
        await asyncio.sleep(20)
        print("меняем аватарку")
        await client(UploadProfilePhotoRequest(file))

    except Exception as ex:
        print(ex)
        print("Не смогли поменять аватар")


    ####
    voronka_count=0
    while True:

        count +=1
        print(f'iteration:{count} for {int(me.id)}')
        task_count = session.query(Task).filter((Task.sender_id == me.id)).count()
        if task_count > 0:
            print(f'Есть {task_count} задания, приступаем к выполнению')
            task = session.query(Task).filter((Task.sender_id == me.id)).first()
            session.commit()
            if task.type == 'send_message':
                try:
                    await asyncio.sleep(task.delay_before)
                    await client.send_message(task.receipient_id, task.data)
                    await asyncio.sleep(task.delay_after)
                    session.query(Task).filter(Task.task_id == task.task_id).delete()


                    print(f"{me.id}->{task.receipient_id} {task.data}")
                except Exception as ex:
                    check_restriction(me, ex)
                    session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
                        {'restricted': 1})
                    session.commit()
                    print(ex)

            if task.type == 'join_chat':
                try:
                    voronka_count += 1
                    print(f"Try to join chat {task.receipient_id}")
                    from telethon.tl.functions.channels import JoinChannelRequest
                    await asyncio.sleep(task.delay_before)
                    await client(JoinChannelRequest(task.receipient_id))
                    print(f"{me.id} joined {task.receipient_id}")
                    await asyncio.sleep(task.delay_after)
                    session.query(Task).filter(Task.task_id == task.task_id).delete()
                    session.commit()
                except Exception as ex:
                    check_restriction(me,ex)
                    session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
                        {'restricted': 1})
                    session.commit()
                    print(ex)







        await asyncio.sleep(2)
        acc = session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).first()
        session.commit()

        if acc.restricted == 1:
            print('account restricted, breacking')
            session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
                {'action': '-'})
            session.commit()
            await leave_all_chats(client, me)
            break
        if acc.deleted == 1:
            print('account deleted, breacking')
            session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
                {'action': '-', 'work': 0})
            session.commit()
            break
        if invite_count >= 20:
            print('invite_count limit exeded, breaking')
            await leave_all_chats(client, me)
            break

        if voronka_count > 20:
            break

    session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
        {'online': 0, 'work':0})
    session.commit()


async def holivar_handle(client):
    @client.on(events.NewMessage)
    async def my_event_handler(event):

        try:
            reply = get_reply(event.raw_text, me)


            if reply != False:
                try:
                    print(f"[{event.chat_id}] {event.raw_text}")
                except Exception as ex:
                    print(ex)

                await asyncio.sleep(random.randint(20, 40))
                await event.reply(reply)
        except Exception as ex:
            print(ex)


    await asyncio.sleep(20)
    await client.start()
    me = await client.get_me()
    await holivar_controller(client,me)

def holivar():
    from ftelethon import get_account_from_db
    from ftelethon import get_client
    from ftelethon import update_account_id

    while True:

        account_from_db = get_account_from_db_holivar()
        account = account_from_db
        try:
            client = get_client(account)
            me = client.get_me()
            session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
                {'online': 1})
            update_account_id(me, account)
            with client:
                client.loop.run_until_complete(holivar_handle(client))
        except Exception as ex:
            print("Клиент не запустился")
            print(f"Клиент {account.telegram_id} не запустился, ставим метку об удалении")
            session.query(Telegram_account).filter(Telegram_account.telegram_id == account.telegram_id).update(
                {'deleted': 1})
            session.commit()
        time.sleep(20)

