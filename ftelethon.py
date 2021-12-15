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

from models.autoria_item import Autoria_item
from models.phone import Phone

from database import Base,session,engine

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
        result =  session.query(Telegram_account).all()
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


async def do_something(client):
    #await client.send_message('@goldjgold', 'Привет')
    res = session.query(Autoria_item,Phone,Car).filter(Autoria_item.tel_id == Phone.phone_id).filter(Autoria_item.car_id == Car.car_id).filter(Autoria_item.sold == 0).offset(700).limit(100000).all()

    me = await client.get_me()
    for row in res:

        try:

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
                message = f"{row[0].person_name}, добрый день!"
            else:
                message = f"Привет!"

            await client.send_message(reciepient_id, message)
            print(f"{me.id} -> {reciepient_id}: {message}")
            message = f"{row[2].name} еще продается?"
            await asyncio.sleep(2)
            await client.send_message(reciepient_id, message)
            print(f"{me.id} -> {reciepient_id}: {message}")
            await asyncio.sleep(120)

        except Exception as ex:
            print(result)
            print(f'[{ex}]{row[1].tel} has no telegram account')
            await client.send_message('@SpamBot', '/start')

            f = open("noaccount.txt", 'w+')
            f.write(f"{row[1].tel}\n")
            f.close()
            await asyncio.sleep(10)











        me = await client.get_me()
        #print(vars(client))


async def telegram_autorespond_handle(client):
    @client.on(events.NewMessage)
    async def my_event_handler(event):
        q = []
        q.append("Какая актуальная цена?")
        q.append("Поторговаться сможем?")
        q.append("а где машину посмотреть можно?")
        q.append("какие у нее датали со шпаклей крашены?")
        q.append("А вы не в курсе, без вакцинации пускают в Мрео cейчас?")
        q.append("Сын бот скинул @mreo_pass_ua_bot, генерирует любые ПцР тесты, если шо, прорвемся")
        q.append("Завтра наберу по просмотру машины вас")


        sender = await event.get_sender()
        messages = client.iter_messages(sender.id)
        me = await client.get_me()
        incoming_count = 0
        print(f"{sender.id} -> {me.id}: {event.raw_text}")



        lines = []
        async for message in messages:

            lines.append(f"{sender.id} -> {me.id}: {message.text}")
            if message.sender_id == me.id:
                incoming_count += 1

        f = open(f"dialogs/{me.id}_{sender.id}.txt", 'w+')
        f.seek(0)
        for line in lines:
            f.write(f"{line}\n")
        f.truncate()
        f.close()

        async def send_q_message(incoming_count, messages, sender_id):
            if incoming_count>=1 and incoming_count <= 7 and sender_id != 178220800:
                incoming_count -= 1
                flag = 0
                async for message in messages:
                    if message.text.strip() == q[incoming_count].strip():
                        flag += 1
                if flag == 0:
                    await asyncio.sleep(5)
                    await client.send_message(sender_id, q[incoming_count])
                    print(f"{me.id} -> {sender_id}: {q[incoming_count]}")


        await  send_q_message(incoming_count, messages, sender.id)





        #print(f'incoming count: {incoming_count}')



    me = await client.get_me()
    print(me.stringify())
    await  do_something(client)





def autorespond(client):
    with client:
        client.loop.run_until_complete(telegram_autorespond_handle(client))