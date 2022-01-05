from telethon import functions, types
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, PeerUser, PeerChat, PeerChannel, User, Channel, Chat
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from database import Base,session,engine

def get_reply(text):
    pass

def get_client(account):
    from fglobal import get_one_proxy
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
            proxy = get_one_proxy()
            session.query(Telegram_account).filter(Telegram_account.telegram_id == account.telegram_id).update({'proxy': proxy.host})
            session.commit()
        else:
            proxy = session.query(Proxy).filter(Proxy.host == account.proxy).first()
    print(f"Starting using {proxy.host}")
    if  proxy.port == 45786:
        proxy.port = 45785
    client = TelegramClient(f"taccounts/{account.session_file}", api_id=account.app_id, api_hash=account.app_hash,
                            proxy=(socks.HTTP, proxy.host, proxy.port, False, proxy.login, proxy.password))
    client.connect()
    if not client.is_user_authorized():
        try:
            client.send_code_request(account.session_file)
            client.start()
        except telethon.errors.rpc_error_list.PhoneNumberBannedError:
            print("Phone number is banned.")
            client.disconnect()
            return False
    else:
        return client

async def holivar_controller(client,me):
    session.query(Telegram_account).filter(Telegram_account.telegram_user_id == int(me.id)).update({'action': 'holivar', 'work': 2})
    session.commit()
    count = 0
    tasks = session.query(Task).filter(Task.sender_id == me.username).filter(Task.done == 0).all()
    print(f"Tasl len:{len(tasks)}")
    invite_count = 0
    while True:
        count +=1
        print(f'iteration:{count} for {int(me.id)}')
        task_count = session.query(Task).filter((Task.sender_id == me.id) | (Task.sender_id == 'all')).count()
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


        time.sleep(2)
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

async def holivar_handle(client):
    @client.on(events.NewMessage)
    async def my_event_handler(event):
        reply = get_reply(event.raw_text)
        if reply != False:
            await event.reply(reply)


    await asyncio.sleep(20)
    client.start()
    me = await client.get_me()
    print(me.stringify())
    await holivar_controller(client,me)

def holivar():

    account_from_db = get_account_from_db()
    account = account_from_db
    try:
        client = get_client(account)
        me = client.get_me()
        update_account_id(me, account)
        with client:
             client.loop.run_until_complete(holivar_handle(client))
    except Exception as ex:
        print("Клиент не запустился")
        print(ex)