from telethon import TelegramClient, sync
from telethon import events
from telethon import functions, types
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, PeerUser, PeerChat, PeerChannel, User, Channel, Chat
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from tqdm import tqdm
import time
import asyncio
import getopt, glob, os, sys, json
import random
import socks
from os import walk

def get_telergam_account():
    dir_name = 'taccounts'
    sessions = []
    for (dirpath, dirnames, filenames) in walk(dir_name):
        for file in filenames:
            file_data = file.split('.')
            if file_data[1]=='session':
                sessions.append(file_data[0])
    return sessions
