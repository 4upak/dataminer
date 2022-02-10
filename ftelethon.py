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

def get_hello_text():
    f = open("hello.txt", "r")
    lines = f.readlines()
    f.close()
    return lines[random.randrange(0, len(lines)-1)]

async def leave_all_chats(client,me):
    try:
        rows = session.query(Telegram_account_groups).filter(Telegram_account_groups.telegram_id == me.id).all()
        if len(rows) >0:
            for row in rows:
                entity = await client.get_entity(row.chat_id)
                await asyncio.sleep(60)
                await client.delete_dialog(entity.id)
                print(f'Deleting {entity.id}')

        session.query(Telegram_account_groups).filter(Telegram_account_groups.telegram_id == me.id).delete()
        session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False

def get_account_info(account):
    try:
        f = open(f"taccounts/{account}.json", "r")
        with f as read_file:
            return json.load(read_file)
    except Exception as ex:
        print(ex)
        return False

def get_telergam_accounts_from_dir():
    dir_name = 'taccounts'
    sessions = []
    for (dirpath, dirnames, filenames) in walk(dir_name):
        for file in filenames:
            file_data = file.split('.')
            if file_data[1]=='session':
                sessions.append(file_data[0])
    return sessions

def create_telegram_accounts_in_db():
    Base.metadata.create_all(engine)
    accounts = get_telergam_accounts_from_dir()

    existing_accounts = session.query(Telegram_account.session_file).all()
    existing_accounts_set = set()
    for account in existing_accounts:
        existing_accounts_set.add(account[0])

    new_accounts = set(accounts) - existing_accounts_set
    count = 0
    for account in new_accounts:
        data = get_account_info(account)

        data['telegram_user_id'] = 0
        data['phone_id'] = 1
        data['proxy'] = '-'


        tg = Telegram_account(data)
        session.add(tg)

        count+=1
    try:
        session.commit()
    except Exception as ex:
        print(ex)
        return False
    return count

def get_account_from_db():
    try:
        result =  session.query(Telegram_account).filter(Telegram_account.deleted==0).filter(Telegram_account.work==0).filter(Telegram_account.restricted==0).filter(Telegram_account.online==0).filter(Telegram_account.action=='-').first()
        session.query(Telegram_account).filter(Telegram_account.telegram_id == result.telegram_id).update({'work': 2})
        session.commit()


    except Exception as ex:
        print(ex)
        return False

    return result

def get_client(account):

    from fglobal import get_free_proxy
    proxy = '-'
    print("Аккаунт:")
    print(account)
    if account.proxy == '-':
        proxy = get_one_proxy()
        account.proxy = proxy.host
        session.add(account)
        session.commit()

    else:
        count = session.query(Proxy).filter(Proxy.host == account.proxy).count()
        if count == 0:
            print("Proxy expired")
            proxy = get_free_proxy()
            session.query(Telegram_account).filter(Telegram_account.telegram_id == account.telegram_id).update({'proxy': proxy.host})
            session.commit()
        else:
            proxy = session.query(Proxy).filter(Proxy.host == account.proxy).first()

        online_proxy_flag = session.query(Telegram_account).filter(Telegram_account.proxy == proxy.host).filter(Telegram_account.online == 1).count()
        print(f"online_proxy_flag: {online_proxy_flag}")
        if online_proxy_flag > 0:
            print("Proxy is online, changing....")
            proxy = get_free_proxy()
            session.query(Telegram_account).filter(Telegram_account.telegram_id == account.telegram_id).update(
                {'proxy': proxy.host})
            session.commit()





    print(f"Starting using {proxy.host}")
    if  proxy.port == 45786:
        proxy.port = 45785
    try:
        client = TelegramClient(f"taccounts/{account.session_file}", api_id=account.app_id, api_hash=account.app_hash,
                            proxy=(socks.HTTP, proxy.host, proxy.port, False, proxy.login, proxy.password))
        client.connect()
    except Exception as ex:
        print("Session is banned.")
        print(str(ex))
        session.query(Telegram_account).filter(Telegram_account.telegram_id == account.telegram_id).update(
            {'deleted': 1})
        session.commit()
        client.disconnect()
        return False

    else:
        return client

def update_account_id(me,account):
    account.telegram_user_id = me.id
    try:
        session.add(account)
        session.flush()
        session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False

def check_work_time():
    while True:
        current_time = datetime.now().time()
        hour = int(str(current_time).split(":")[0])
        if hour >= 22 or hour <= 8:
            print("Время не летное, засыпаем на час")
            time.sleep(3600)
        else:
            break

async def autorespond_controller(client,me):


    offset = random.randint(0, 100000)
    global_count = 0
    wrong_phone_count = 0

    while True:
        check_work_time()
        global_count += 1
        wrong_phone_count = 0

        row = session.query(Phone, Autoria_item, Car) \
            .filter(Phone.telegram_checked == 0) \
            .filter(Phone.phone_id == Autoria_item.tel_id) \
            .filter(Autoria_item.sold == 0) \
            .filter(Car.car_id == Autoria_item.car_id) \
            .offset(offset).first()

        timestamp = int(time.time())
        session.query(Autoria_item).filter(Autoria_item.item_id == row[1].item_id).update(
            {'telegram_contact': timestamp})
        session.commit()
        try:

            #contact = await client.get_entity()
            print(f"Checking {row[0].tel}")
            contact = InputPhoneContact(client_id=0, phone=row[0].tel, first_name="", last_name="")
            result = await client(ImportContactsRequest([contact]))
            result = result.to_dict()
            reciepient_id = result['imported'][0]['user_id']

            session.query(Phone).filter(Phone.phone_id == row[0].phone_id).update({'telegram_id': reciepient_id, 'telegram_checked':1})
            session.commit()
            if row[1].person_name != '-':
                name_list = row[1].person_name.split(" ")
                if len(name_list)>0:
                    message = f"{name_list[0]}, добрый день! {row[2].name} еще продается?"
                else:
                    message = f"{row[1].person_name}, добрый день! {row[2].name} еще продается?"
            else:
                message = f"Привет! {row[2].name} еще продается?"
            print(f"[{global_count}] -> {reciepient_id}: {message}")
            dialog = Telegram_dialog(me.id, reciepient_id, message)
            session.add(dialog)
            session.commit()
            await client.send_message(reciepient_id, message)
            wrong_phone_count = 0
            await asyncio.sleep(1800)

        except Exception as ex:
            wrong_phone_count += 1
            print(f'[{wrong_phone_count}][{ex}]{row[0].tel} has no telegram account')
            session.query(Phone).filter(Phone.phone_id == row[0].phone_id).update({'telegram_checked': 1})
            session.commit()

            await asyncio.sleep(600)

        if wrong_phone_count > 5:
            await client.send_message('@SpamBot', '/start')
            #session.query(Telegram_account).filter(Telegram_account.telegram_id == me.id).update({'restricted': 1})

        acc = session.query(Telegram_account).filter(Telegram_account.telegram_user_id == me.id).first()

        if acc.restricted == 1:
            print("В базе аккуант отмечен как ограничен по сообщениям")
            print("Ждем еще 1 час и выходим")
            await asyncio.sleep(3600)
            break

async def autorespond_handle(client):
    @client.on(events.NewMessage)
    async def my_event_handler(event):
        sender = await event.get_sender()
        async def get_incoming_count(sender_id, reciepient_id):
            res = session.query(Telegram_dialog).filter(Telegram_dialog.sender_id == sender_id).filter(
                Telegram_dialog.recipient_id == reciepient_id).all()
            return len(res)

        async def check_account_ban(event):
            print("Спамбот прислал ответ")
            if re.search('limited', event.raw_text) or re.search('moderator', event.raw_text):
                print("Забанилось добавлем метку в базу:(")
                session.query(Telegram_account).filter(Telegram_account.telegram_id == me.id).update({'restricted': 1})
            else:
                print("Все ок, продолжаем")

        async def send_q_message(incoming_count, sender_id):

            if incoming_count >= 1 and incoming_count <= len(q) + 1 and sender_id != 178220800:
                incoming_count -= 1
                try:
                    dialog = Telegram_dialog(me.id, sender_id, q[incoming_count])
                    session.add(dialog)
                    session.commit()
                    await asyncio.sleep(10)
                    await client.send_message(sender_id, q[incoming_count])
                    print(f"{me.id} -> {sender_id}: {q[incoming_count]}")
                except Exception as ex:
                    print(ex)
        if int(session.query(Phone).filter(Phone.telegram_id == sender.id).count()) > 0:
            incoming_count = await get_incoming_count(me.id, sender.id)
            incoming_count = int(incoming_count)

            q = []
            q.append("Что у машины по кузаву? На стойках и порогах есть шпаклевка")
            q.append("Какая акутуальная цена")
            q.append("Поторговаться сможем?")
            q.append("Где машину посмотерть можно?")
            q.append("А вы не в курсе, без вакцинации пускают в Мрео cейчас?")
            q.append("Завтра наберу по просмотру?")


            if sender.id != 178220800 and incoming_count>0:
                print(f"{sender.id} -> {me.id}: {event.raw_text}")
                dialog = Telegram_dialog(sender.id, me.id, event.raw_text)
                session.add(dialog)
                session.commit()
            else:
                await check_account_ban(event)


            if incoming_count <= len(q)+1 and incoming_count>0:
                await send_q_message(incoming_count, sender.id)

    me = await client.get_me()
    print(me.stringify())
    await  autorespond_controller(client, me)

def autorespond(client):
    with client:
        client.loop.run_until_complete(autorespond_handle(client))
#################################################################################################
#################################################################################################
#################################################################################################

def save_dialog(sender_id, receipient_id, text):
    try:
        dialog = Telegram_dialog(sender_id, receipient_id, text)
        session.add(dialog)
        session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False

async def join_chat(telegram_id, chat_id,client):
    from telethon.tl.functions.channels import JoinChannelRequest
    try:
        chat_invited = session.query(Telegram_account_groups).filter(Telegram_account_groups.telegram_id == telegram_id).filter(Telegram_account_groups.chat_id == chat_id).count()
        if chat_invited == 0:
            await client(JoinChannelRequest(chat_id))
            print(f"{telegram_id} вступил в {chat_id}")
            account_chat_mixin = Telegram_account_groups(telegram_id, chat_id)
            session.add(account_chat_mixin)
            session.commit()
        return True

    except Exception as ex:
        print(ex)
        return False

async def warming_up_controller(client,me):
    try:
        client.start()
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update({'action': 'warmin_up', 'work': 2})
        session.commit()
        count = 0
        tasks = session.query(Task).filter(Task.sender_id == me.username).filter(Task.done == 0).all()
        print(f"Tasl len:{len(tasks)}")
        invite_count = 0
        while True:
            count +=1
            print(f'iteration:{count} for {int(me.id)}')
            task_count = session.query(Task).filter((Task.sender_id == me.username) | (Task.sender_id == 'all')).count()
            if task_count > 0:
                print(f'Есть {task_count} задания, приступаем к выполнению')
                task = session.query(Task).filter((Task.sender_id == me.username) | (Task.sender_id == 'all')).first()
                session.commit()
                if task.type == 'send_message':
                    try:
                        time.sleep(task.delay_before)
                        await client.send_message(task.receipient_id, task.data)
                        time.sleep(task.delay_after)
                        session.query(Task).filter(Task.task_id == task.task_id).delete()
                        save_dialog(me.id, task.receipient_id, task.data)
                        print(f"{me.id}->{task.receipient_id} {task.data}")
                    except Exception as ex:
                        print(ex)

                if task.type == 'join_chat':
                    try:
                        print(f"Try to join chat {task.receipient_id}")
                        from telethon.tl.functions.channels import JoinChannelRequest
                        time.sleep(task.delay_before)
                        join_chat(me.id, task.receipient_id, client)

                        print(f"{me.id} joined {task.receipient_id}")
                        time.sleep(task.delay_after)
                        session.query(Task).filter(Task.task_id == task.task_id).delete()
                        session.commit()
                    except Exception as ex:
                        print(ex)

                if task.type == 'invite_to_chat':
                    try:
                        print(f'[{invite_count}]{me.id} Try to invite {task.receipient_id} to {task.data}')
                        from telethon.sync import TelegramClient
                        from telethon import functions, types
                        session.query(Task).filter(Task.task_id == task.task_id).delete()
                        session.commit()

                        await join_chat(me.id, task.data, client)
                        await asyncio.sleep(task.delay_before)

                        user_entity = await client.get_entity(task.receipient_id)
                        target_group_entity = await client.get_entity(task.data)

                        result = await client(functions.channels.InviteToChannelRequest(
                            channel= target_group_entity,
                            users= [user_entity]
                        ))
                        await asyncio.sleep(task.delay_after)

                        invite_count+=1
                        print(f'{task.receipient_id} добавлен в  {task.data}')

                    except Exception as ex:
                        print(ex)
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






                        await asyncio.sleep(task.delay_after)
                        session.query(Task).filter(Task.task_id == task.task_id).delete()
                        session.commit()


            time.sleep(2)
            acc = session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).first()
            session.commit()

            if acc.restricted == 1:
                print('account restricted, breacking')
                session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
                    {'action': '-', 'online':0})
                session.commit()
                await leave_all_chats(client, me)
                break

            if acc.deleted == 1:
                print('account deleted, breacking')
                break

            if invite_count >= 20:
                print('invite_count limit exeded, breaking')
                await leave_all_chats(client, me)
                break
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'action': '-', 'work': 0, 'online':0})
        session.commit()
    except KeyboardInterrupt:
        session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
            {'action': '-', 'work': 0, 'online':0})
        session.commit()
        print("cleint disconected by keyboard interrupt")

async def warming_up_handle(client):
    @client.on(events.NewMessage)
    async def my_event_handler(event):
        try:
            sender = await event.get_sender()
            count = session.query(Telegram_account).filter(Telegram_account.telegram_user_id == sender.id).count()
            if count > 0:
                print(f"{sender.id} -> {me.id}: {event.raw_text}")
                save_dialog(sender.id, me.id, event.raw_text)
        except Exception as ex:
            print("пришло сообщение без сендера")

    await asyncio.sleep(20)
    client.start()

    me = await client.get_me()
    print(me.stringify())
    await warming_up_controller(client,me)


def warming_up():

    while True:
        account_from_db = get_account_from_db()
        account = account_from_db
        try:
            client = get_client(account)
            me = client.get_me()
            session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update(
                {'online': 1})
            session.commit()
            update_account_id(me, account)


            with client:

                client.loop.run_until_complete(warming_up_handle(client))
        except Exception as ex:
            print(f"Клиент {account.telegram_id} не запустился, ставим метку об удалении")
            session.query(Telegram_account).filter(Telegram_account.telegram_id == account.telegram_id).update(
                {'deleted': 1})
            session.commit()