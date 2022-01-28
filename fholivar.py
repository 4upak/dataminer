from telethon import events
import asyncio
import re
import random
import time
from database import Base,session,engine
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from os import walk
from models.holivar import Holivar_unit
from models.telegram_account import Telegram_account
from models.task import Task
from models.funnel import Funnel_unit
from models.chat import Chat
from sqlalchemy import func
import json
import datetime
import calendar
from telethon import events, utils
import os
from models.action import Action


def get_account_from_db_holivar(funnel_name):
    try:
        result =  session.query(Telegram_account).filter(Telegram_account.deleted==0).filter(Telegram_account.message_restricted==0).filter(Telegram_account.online==0).filter(Telegram_account.action=='-').first()
        session.query(Telegram_account).filter(Telegram_account.telegram_id == result.telegram_id).update({'work': 2, 'action': f"holivar_{funnel_name}"})
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

def check_restriction(me,ex, funnel_name):
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

    if re.search("Another reason may be that you were banned from it", str(ex)):
        action_to_do = Action('reload_funnel', 'one of account was banned from current channel', funnel_name)
        session.add(action_to_do)
        session.commit()

    if re.search("can't write in this chat", str(ex)):
        action_to_do = Action('reload_funnel', 'one of account was banned from current channel', funnel_name)
        session.add(action_to_do)
        session.commit()

    if re.search("seconds is required before sending another message in this chat", str(ex)):
        action_to_do = Action('reload_funnel', 'one of account was banned from current channel', funnel_name)
        session.add(action_to_do)
        session.commit()


        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'restricted': 1, 'message_restricted': 1})
        session.commit()



    return True

async def change_name(client):
    f = open("fio.txt", "r")
    lines = f.readlines()
    f.close()
    fio = lines[random.randrange(0, len(lines) - 1)]
    name = fio.split(' ')[1]
    lastname = fio.split(' ')[0]
    await client(UpdateProfileRequest(first_name=name, last_name=lastname))
    print(f"аккаунт изменил имя на:{name} {lastname}")
    return True

async def change_avatar(client):
    avatars = []
    for (dirpath, dirnames, filenames) in walk('avatars'):
        for file in filenames:
            avatars.append(file)
    new_avatar = avatars[random.randrange(0, len(avatars) - 1)]
    file_name = f"avatars/{new_avatar}"
    print(file_name)
    print("Загружаем файл")
    file = await client.upload_file(file_name)
    await asyncio.sleep(20)
    print("меняем аватарку")
    await client(UploadProfilePhotoRequest(file))
    return True

async def holivar_controller(client,me, funnel_name):

    session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update({'action': f'holivar_{funnel_name}', 'work': 2})
    session.commit()
    count = 0
    tasks = session.query(Task).filter(Task.sender_id == me.username).filter(Task.done == 0).all()
    print(f"Колическо заданий в базе:{len(tasks)}")
    invite_count = 0

    #change_name
    try:
        await change_name(client)
    except Exception as ex:
        print(ex)
        print("Имя изменить не смогли")

    await asyncio.sleep(10)

    # change_avatar
    try:
        await change_avatar(client)

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
                    check_restriction(me, ex,funnel_name)
                    session.query(Chat).filter(Chat.chat_login == task.receipient_id).update({'moderation_status': 1})
                    session.query(Task).filter(Task.task_id == task.task_id).delete()
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
                    check_restriction(me,ex,funnel_name)
                    session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
                        {'restricted': 1})
                    session.query(Task).filter(Task.task_id == task.task_id).delete()
                    session.commit()
                    print(ex)

            if task.type == 'send_image':
                try:
                    await asyncio.sleep(task.delay_before)
                    await client.send_file(task.receipient_id, task.data)
                    await asyncio.sleep(task.delay_after)
                    session.query(Task).filter(Task.task_id == task.task_id).delete()
                    session.commit()
                except Exception as ex:
                    check_restriction(me, ex,funnel_name)
                    session.query(Task).filter(Task.task_id == task.task_id).delete()
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
    print("Updating account data (online, work, action)")
    session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
        {'online': 0, 'work':0, 'action':'-'})
    session.commit()


async def holivar_handle(client, funnel_name):
    @client.on(events.NewMessage)
    async def my_event_handler(event):

        sender = await event.get_sender()  # получаем имя юзера
        user_name = utils.get_display_name(sender)  # Имя Юзера

        chat_from = event.chat if event.chat else (await event.get_chat())  # получаем имя группы
        chat_title = utils.get_display_name(chat_from)  # получаем имя группы

        #print(f"sender:{sender.username}, user_name: {user_name}, chat_from: {chat_from.username}, chat_title:{chat_title}, chat_id:{event.chat_id}")

        c = session.query(Chat).filter(Chat.chat_login == chat_from.username).filter(Chat.active == 1).count()
        if c>0:
            try:
                reply = get_reply(event.raw_text, me)


                if reply != False:
                    try:
                        print(f"[{event.chat_id}] {event.raw_text}")
                    except Exception as ex:
                        print(f'Can not check reply for message from {chat_from.username}')

                    await asyncio.sleep(random.randint(20, 40))
                    await event.reply(reply)
            except Exception as ex:
                print(ex)
        else:
            await client.delete_dialog(chat_from)
            print(f"{chat_from.username} has been deleted")


    await asyncio.sleep(20)
    await client.start()
    me = await client.get_me()
    await holivar_controller(client,me, funnel_name)

def holivar(funnel_name):
    from ftelethon import get_account_from_db
    from ftelethon import get_client
    from ftelethon import update_account_id

    while True:

        account_from_db = get_account_from_db_holivar(funnel_name)
        account = account_from_db
        try:
            client = get_client(account)
            me = client.get_me()
            session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
                {'online': 1})
            update_account_id(me, account)
            with client:
                client.loop.run_until_complete(holivar_handle(client, funnel_name))
        except Exception as ex:
            print("Клиент не запустился")
            print(f"Клиент {account.telegram_id} не запустился, ставим метку об удалении")
            session.query(Telegram_account).filter(Telegram_account.telegram_id == account.telegram_id).update(
                {'deleted': 1, 'action': '-', 'online':0})
            session.commit()
        time.sleep(20)

def holivar_check_accounts(funnel_name):
    sleep_count = 0
    error_flag = 0
    while True:
        sleep_count += 1
        if sleep_count > 24:
            break
        acc_count = session.query(Telegram_account).filter(Telegram_account.online == 1).filter(
            Telegram_account.action == f'holivar_{funnel_name}').count()
        session.commit()
        if acc_count != 5:
            return False
        time.sleep(5)

def check_funnel_finish(funnel_name,current_chat):
    count_done = session.query(Holivar_unit).filter(Holivar_unit.done == 1).filter(
        Holivar_unit.funnel_name == funnel_name).count()
    count_mess = session.query(Holivar_unit).filter(Holivar_unit.answer_to_key == 0).filter(
        Holivar_unit.funnel_name == funnel_name).count()
    if count_done == count_mess:
        session.query(Chat).filter(Chat.chat_id == current_chat.chat_id).update(
            {'active': 0, 'active_funnel': '-'})
        session.commit()
        return True
    else:
        return False

def check_releoad_actions(funnel_name,current_chat):
    action_count = session.query(Action).filter(Action.done == 0).filter(Action.funnel_name == funnel_name).count()
    if action_count > 0:
        action = session.query(Action).filter(Action.done == 0).filter(Action.funnel_name == funnel_name).first()
        print(action.comment)
        print(f"Reload funnel {funnel_name} action finded, current funnel stopped")

        session.query(Action).filter(Action.done == 0).filter(Action.funnel_name == funnel_name).update({'done': 1})

        session.query(Chat).filter(Chat.chat_id == current_chat.chat_id).update(
            {'moderation_status': 1, 'active': 0, 'active_funnel': '-'})
        session.commit()
        return True
    else:
        return False

def holivar_main(funnel_name):
    from testing import holivar


    users = []
    needed_account_count = session.query(func.max(Funnel_unit.user_id)).scalar()
    while True:
        current_chat = session.query(Chat).filter(Chat.last_interaction == 0).first()
        chat_to_holivar = current_chat.chat_login

        date = datetime.datetime.utcnow()
        utc_time = calendar.timegm(date.utctimetuple())



        print(f"Активный чат: {chat_to_holivar}")
        while True:
            count = session.query(Telegram_account).filter(Telegram_account.online == 1).filter(
                Telegram_account.action == f'holivar_{funnel_name}').count()
            session.commit()
            print(f"{count} accounts online")
            if count != needed_account_count:
                print(f"Аккаунтов не {needed_account_count} шт")
                print("Ждем запуска аккаунтв")
                time.sleep(5)
            else:
                users = session.query(Telegram_account).filter(Telegram_account.online == 1).filter(
                    Telegram_account.action == f'holivar_{funnel_name}').all()
                random.shuffle(users)
                break
        session.query(Chat).filter(Chat.chat_id == current_chat.chat_id).update({'last_interaction': utc_time, 'active': 1, 'active_funnel': funnel_name})
        session.commit()
        count = 0
        session.query(Holivar_unit).filter(Holivar_unit.funnel_name == funnel_name).delete()
        holivar_units = session.query(Funnel_unit).filter(Funnel_unit.funnel_name == funnel_name).all()
        for unit in holivar_units:
            unit = Holivar_unit(unit.index_id, unit.text_message, unit.json_data, unit.answer_to, users[int(unit.user_id)-1].telegram_user_id, funnel_name)
            session.add(unit)
            count += 1
        session.commit()

        print("Create task to join chat")
        for user in users:
            task = Task('join_chat', user.telegram_user_id, chat_to_holivar, '-')
            task.delay_after = 10
            task.delay_before = 10
            session.add(task)
        session.commit()


        while True:

            count = session.query(Holivar_unit).filter(Holivar_unit.answer_to_key == 0).filter(
                Holivar_unit.done == 0).count()
            session.commit()
            if count > 0:
                print(f"Start hilovar {chat_to_holivar}")
                unit = session.query(Holivar_unit).filter(Holivar_unit.answer_to_key == 0).filter(Holivar_unit.done == 0).filter(Holivar_unit.funnel_name == funnel_name).first()
                print(unit)
                user = session.query(Telegram_account).filter(Telegram_account.telegram_user_id == unit.user_id).first()
                print(user)
                if unit.message != '-':
                    task_sender = Task('send_message', user.telegram_user_id, chat_to_holivar, unit.message)
                    session.add(task_sender)
                    session.query(Holivar_unit).filter(Holivar_unit.unit_id == unit.unit_id).update({'done': 1})
                    session.commit()
                else:
                    if unit.message == '-':
                        print(unit.json_data)
                        data = json.loads(unit.json_data)


                        if data['action'] == 'send_image':
                            task_sender = Task('send_image', user.telegram_user_id, chat_to_holivar, data['data'])
                            session.add(task_sender)
                            session.query(Holivar_unit).filter(Holivar_unit.unit_id == unit.unit_id).update({'done': 1})
                            session.commit()


            print("Sleeping ...")

            if holivar_check_accounts(funnel_name) == False:
                print("Account crashed, relaunch funnel")
                session.query(Chat).filter(Chat.chat_id == current_chat.chat_id).update({'active': 0, 'active_funnel': '-'})
                session.commit()
                break

            if check_releoad_actions(funnel_name, current_chat) == True:
                break

            if check_funnel_finish(funnel_name, current_chat) == True:
                break



