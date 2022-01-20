import sys
import getopt
from fglobal import check_proxy, read_proxy
import time



def update_proxy_list():
    print('Checking proxies')
    check_proxy()
    print(f'We have {len(read_proxy())} valid proxies in proxy list')

def main(argumentList):
    options = "a:h:"
    long_options = []

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-a", "-action", "-act"):
                if currentValue == "base":
                    from autoria import get_all_base
                    from fglobal import check_proxy
                    check_proxy()
                    get_all_base()

                elif currentValue == "accunt_speaking":
                    from database import Base, session, engine
                    from datetime import datetime
                    from models.autoria_item import Autoria_item
                    from models.phone import Phone
                    from models.car import Car
                    from models.task import Task
                    from models.dialog import Telegram_dialog
                    from models.telegram_account import Telegram_account
                    from models.proxy import Proxy
                    import random
                    import re
                    accs = session.query(Telegram_account).filter(Telegram_account.work==2).filter(Telegram_account.action=='warmin_up').all()
                    acc_count = len(accs)-1


                    l = []
                    r = []
                    for i in range(0,acc_count,2):
                        l.append(i)
                        r.append(i+1)

                    def create_task(accs,left_list,right_list):
                        print(len(accs))
                        print(left_list)
                        print(right_list)
                        i=0
                        print(accs)
                        for row in left_list:

                            sender_id = accs[left_list[i]].session_file
                            receipient_id = accs[right_list[i]].session_file
                            i+=1
                            f = open(f"songs/{random.randrange(1, 10)}.txt", "r")
                            lines = f.readlines()
                            f.close()
                            for p in range(0, len(lines) - 1, 2):
                                task_sender = Task('send_message', sender_id, receipient_id, lines[p])
                                task_sender.delay_after = 60
                                task_receipient = Task('send_message', receipient_id, sender_id, lines[p + 1])
                                task_receipient.delay_before = 60
                                session.add(task_sender)
                                session.add(task_receipient)
                                session.commit()

                        while True:
                            tsk_count = session.query(Task).count()
                            session.commit()
                            print(f"tsk_count: {tsk_count}")
                            if tsk_count > 0:
                                time.sleep(60)
                            else:
                                time.sleep(180)
                                break

                    ####################################################################################################
                    left_list = []
                    right_list = []
                    for row_l in l:
                        for j in range(0,len(l),1):
                            left_list.append(l[j])
                            right_list.append(r[j])
                        create_task(accs, left_list, right_list)

                        left_list = []
                        right_list = []
                        r.append(r[0])
                        r.pop(0)

                    for i in range(0,len(l), 1):
                        if i+1<len(l):
                            left_list.append(l[i])
                            right_list.append(l[i+1])
                    create_task(accs, left_list, right_list)

                    left_list = []
                    right_list = []
                    for j in range(0,len(r),1):
                        if j+1<len(r):
                            left_list.append(r[j])
                            right_list.append(r[j + 1])
                    create_task(accs, left_list, right_list)

                    left_list = []
                    right_list = []
















                elif currentValue == "update":
                    from autoria import update_base
                    from fglobal import check_proxy
                    check_proxy()
                    update_base()

                elif currentValue == "check_proxy":
                    from fglobal import check_proxy
                    check_proxy()

                elif currentValue == "telegram":
                    from ftelethon import get_account_from_db, get_client,update_account_id,create_telegram_accounts_in_db, autorespond, leave_all_chats
                    create_telegram_accounts_in_db()
                    account_from_db = get_account_from_db()
                    account = account_from_db
                    client = get_client(account)
                    me = client.get_me()
                    update_account_id(me,account)
                    autorespond(client)

                elif currentValue == "create_accounts":
                    from ftelethon import get_account_from_db, get_client, update_account_id, create_telegram_accounts_in_db, warming_up, leave_all_chats
                    count = create_telegram_accounts_in_db()
                    print(f"{count} accounts created")

                elif currentValue == "warming":
                    from ftelethon import get_account_from_db, get_client, update_account_id, \
                        create_telegram_accounts_in_db, warming_up, leave_all_chats
                    warming_up()



                elif currentValue == "create_base":
                    from models.autoria_item import Autoria_item
                    from models.phone import Phone
                    from models.car import Car
                    from models.dialog import Telegram_dialog
                    from models.proxy import Proxy
                    from models.task import Task
                    from models.telegram_account import Telegram_account
                    from models.holivar import Holivar_unit
                    from models.telegram_account_groups import Telegram_account_groups
                    from database import Base, session, engine
                    Base.metadata.create_all(engine)

                elif currentValue == "invite":
                    from database import Base, session, engine
                    from datetime import datetime
                    from models.autoria_item import Autoria_item
                    from models.phone import Phone
                    from models.car import Car
                    from models.task import Task
                    from models.dialog import Telegram_dialog
                    from models.telegram_account import Telegram_account
                    from models.proxy import Proxy
                    import random
                    import re


                    f = open("usernames.txt", "r")
                    lines = f.readlines()
                    f.close()
                    active_account_username = 'all'
                    chat_to_invite_list = [
                        'lanka_free_me',
                        'lanka_free_you',
                        'lanka_free_time',
                        'lanka_free_new',
                        'lanka_free'
                    ]

                    count = 0
                    for line in lines:
                        count += 1
                        username_to_invite = line.strip()
                        chat_to_invite = chat_to_invite_list[random.randrange(0, len(chat_to_invite_list))]
                        task = Task('invite_to_chat', active_account_username, username_to_invite, chat_to_invite)
                        task.delay_bofore = 20
                        task.delay_after = 30
                        session.add(task)
                        session.commit()

                elif currentValue == "holivar":
                    from database import Base, session, engine
                    import fholivar
                    import time
                    from testing import holivar
                    from models.holivar import Holivar_unit
                    from models.telegram_account import Telegram_account
                    from models.task import Task
                    import random


                    f = open("chats.txt", "r")
                    lines = f.readlines()
                    f.close()




                    users = []
                    while True:
                        chat_to_holivar = lines[random.randrange(0, len(lines) - 1)]
                        print(f"Ебашим {chat_to_holivar}")
                        while True:
                            count = session.query(Telegram_account).filter(Telegram_account.online==1).filter(Telegram_account.action=='holivar').count()
                            session.commit()
                            print(f"Аккаунтов в онлайне {count}")
                            if count != 5:
                                print("Аккаунтов не 5 шт")
                                print("Ждем запуска аккаунтв")
                                time.sleep(5)
                            else:
                                users = session.query(Telegram_account).filter(Telegram_account.online == 1).filter(Telegram_account.action == 'holivar').all()
                                random.shuffle(users)
                                break
                        print(users)
                        #ебашим диалог в базу
                        count = 0
                        session.query(Holivar_unit).delete()
                        for row in holivar:
                            unit = Holivar_unit(row['id'], row['mess'], row['answer_to'], users[int(row['user_id'])-1].telegram_user_id)
                            session.add(unit)
                            count += 1
                        session.commit()

                        print("Добавляем задание на вступление в чат")
                        for user in users:
                            task = Task('join_chat', user.telegram_user_id, chat_to_holivar, '-')
                            task.delay_after = 10
                            task.delay_before = 10
                            session.add(task)
                        session.commit()

                        count = session.query(Telegram_account).filter(Telegram_account.online == 1).filter(Telegram_account.action == 'holivar').count()

                        while True:

                            count = session.query(Holivar_unit).filter(Holivar_unit.answer_to_key == 0).filter(Holivar_unit.done == 0).count()
                            session.commit()
                            if count>0:
                                print("Начинаем холиварить")
                                unit = session.query(Holivar_unit).filter(Holivar_unit.answer_to_key == 0).filter(Holivar_unit.done == 0).first()
                                print(unit)
                                user = session.query(Telegram_account).filter(Telegram_account.telegram_user_id == unit.user_id).first()
                                print(user)

                                task_sender = Task('send_message', user.telegram_user_id, chat_to_holivar, unit.message)
                                session.add(task_sender)
                                session.query(Holivar_unit).filter(Holivar_unit.unit_id == unit.unit_id).update({'done': 1})
                                session.commit()

                            print("Засыпаем")
                            sleep_count = 0
                            error_flag = 0
                            while True:
                                sleep_count+=1
                                if sleep_count>24:
                                    break
                                acc_count = session.query(Telegram_account).filter(Telegram_account.online == 1).filter(
                                    Telegram_account.action == 'holivar').count()
                                session.commit()
                                if acc_count != 5:
                                    error_flag =1
                                    break
                                time.sleep(5)
                            if error_flag ==1:
                                print("Наебнулся аккаунт, стопаем воронку")
                                break



                            count_done = session.query(Holivar_unit).filter(Holivar_unit.done == 1).count()
                            count_mess = session.query(Holivar_unit).filter(Holivar_unit.answer_to_key == 0).count()
                            if count_done == count_mess:
                                break






                elif currentValue == "testing":
                    from os import walk
                    import random
                    avatars = []
                    for (dirpath, dirnames, filenames) in walk('avatars'):
                        for file in filenames:
                            avatars.append(file)
                    print(avatars)
                    new_avatar = avatars[random.randrange(0, len(avatars) - 1)]
                    print(new_avatar)


                elif currentValue == "holivar_client":
                    from fholivar import holivar
                    holivar()








    except getopt.error as err:
        print(str(err))

if __name__ == '__main__':
    main(sys.argv[1:])
