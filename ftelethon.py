import json
from os import walk
from models.autoria_item import Autoria_item, Phone, Car
from models.telegram_account import Telegram_account
from telethon import TelegramClient, sync
from models.proxy import Proxy
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

from database import Base,session,engine

def leave_all_chats(client):
    for dialog in client.iter_dialogs():

        entity = client.get_entity(dialog.entity)
        if isinstance(entity, Chat):
            client.delete_dialog(entity.id)
            print(f'Deleting {entity.id}')

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
        result =  session.query(Telegram_account).filter(Telegram_account.deleted==0).filter(Telegram_account.work==0).first()
        session.query(Telegram_account).filter(Telegram_account.telegram_id == result.telegram_id).update({'work': 2})
        session.commit()


    except Exception as ex:
        print(ex)
        return False

    return result

def get_client(account):

    from fglobal import get_one_proxy

    if account.proxy!='-':
        proxy = session.query(Proxy).filter(Proxy.host == account.proxy).first()
        if isinstance(proxy,Proxy):
            pass
        else:
            proxy = get_one_proxy()
            account.proxy = proxy.host
            session.add(account)
            session.commit()
    else:
        proxy = get_one_proxy()
        account.proxy = proxy.host
        session.add(account)
        session.commit()


    print(vars(proxy))
    if  proxy.port == 45786:
        proxy.port = 45785
    client = TelegramClient(f"taccounts/{account.session_file}", api_id=account.app_id, api_hash=account.app_hash,
                            proxy=(socks.HTTP, proxy.host, proxy.port, False, proxy.login, proxy.password))
    client.connect()
    client.start()
    if not client.is_user_authorized():
        try:
            client.get_me()
        except telethon.errors.rpc_error_list.PhoneNumberBannedError:
            print("Phone number is banned.")
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

async def do_something(client,me):
    #await client.send_message('@goldjgold', 'Привет')

    global_count = random.randint(0, 100000)
    while True:

        while True:
            current_time = datetime.now().time()
            hour = int(str(current_time).split(":")[0])
            if hour >= 22 or hour <= 8:
                print("Время не летное, засыпаем на час")
                await asyncio.sleep(3600)




        global_count += 1
        res = session.query(Autoria_item, Phone, Car).filter(Autoria_item.tel_id == Phone.phone_id).filter(
            Autoria_item.car_id == Car.car_id).filter(Autoria_item.sold == 0).filter(Autoria_item.telegram_contact == 0).offset(global_count).limit(1).all()

        timestamp = int(time.time())
        row = res[0]
        session.query(Autoria_item).filter(Autoria_item.item_id == row[0].item_id).update(
            {'telegram_contact': timestamp})
        session.commit()
        try:
            dialog = Telegram_dialog(me.id, 178220800, '/start')
            session.add(dialog)
            session.commit()
            await client.send_message('@SpamBot', '/start')
            #contact = await client.get_entity()
            print(f"Checking {row[1].tel}")
            contact = InputPhoneContact(client_id=0, phone=row[1].tel, first_name="", last_name="")
            result = await client(ImportContactsRequest([contact]))
            result = result.to_dict()
            reciepient_id = result['imported'][0]['user_id']
            phone = Phone(row[1].tel)
            phone.phone_id = row[1].phone_id
            phone.telegram_id = reciepient_id
            session.query(Phone).filter(Phone.phone_id == row[1].phone_id).update({'telegram_id': reciepient_id})
            session.commit()


            if row[0].person_name != '-':
                message = f"{row[0].person_name}, добрый день! {row[2].name} еще продается?"
            else:
                message = f"Привет! {row[2].name} еще продается?"

            print(f"[{global_count}] -> {reciepient_id}: {message}")

            dialog = Telegram_dialog(me.id, reciepient_id, message)
            session.add(dialog)
            session.commit()
            await client.send_message(reciepient_id, message)
            await asyncio.sleep(600)

        except Exception as ex:
            print(f'[{ex}]{row[1].tel} has no telegram account')

            print("Шлем сообщение спамботу")
            dialog = Telegram_dialog(me.id, 178220800, '/start')
            session.add(dialog)
            session.commit()
            await client.send_message('@SpamBot', '/start')

            await asyncio.sleep(100)


        acc = session.query(Telegram_account).filter(Telegram_account.telegram_user_id == me.id).first()

        if acc.restricted == 1:

            print("В базе аккуант отмечен как ограничен по сообщениям")
            print("Ждем еще 1 час и выходим")
            await asyncio.sleep(3600)
            break




#def iter_dialog(contact_id):
#    res = session.query(Telegram_dialog).filter(((Telegram_dialog.sender_id == contact_id)) | (Telegram_dialog.recipient_id==contact_id)) & ((Telegram_dialog.recipient_idsender_id == contact_id)) | (Telegram_dialog.sender_id ==contact_id))).all()
#    return res






async def telegram_autorespond_handle(client):
    @client.on(events.NewMessage)

    async def my_event_handler(event):

        sender = await event.get_sender()

        if sender.id != 178220800:
            dialog = Telegram_dialog(sender.id, me.id, event.raw_text)
            session.add(dialog)
            session.commit()

        q = []
        q.append("Что у машины по кузаву? На стойках и порогах есть шпаклевка")
        q.append("Какая акутуальная цена")
        q.append("Поторговаться сможем?")
        q.append("Где машину посмотерть можно?")
        q.append("А вы не в курсе, без вакцинации пускают в Мрео cейчас?")
        q.append("Завтра наберу по просмотру?")


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



        incoming_count = await get_incoming_count(me.id, sender.id)
        incoming_count = int(incoming_count)
        if sender.id != 178220800:
            print(f"{sender.id} -> {me.id}: {event.raw_text}")
        else:
            await check_account_ban(event)


        async def send_q_message(incoming_count, sender_id):

            if incoming_count>=1 and incoming_count <= len(q)+1 and sender_id != 178220800:
                incoming_count -= 1

                dialog = Telegram_dialog(me.id, sender_id, q[incoming_count])
                session.add(dialog)
                session.commit()
                await asyncio.sleep(10)
                await client.send_message(sender_id, q[incoming_count])

                print(f"{me.id} -> {sender_id}: {q[incoming_count]}")


        if incoming_count <= len(q)+1 and incoming_count>0:
            await send_q_message(incoming_count, sender.id)


    me = await client.get_me()
    print(me.stringify())
    await  do_something(client, me)

def autorespond(client):
    with client:
        client.loop.run_until_complete(telegram_autorespond_handle(client))