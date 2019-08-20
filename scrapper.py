import logging     
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import (InputMessagesFilterMusic, InputMessagesFilterContacts, InputMessagesFilterUrl
                               InputMessagesFilterPhotos, InputMessagesFilterVideo, InputMessagesFilterDocument)
from telethon.errors.rpcerrorlist import FloodWaitError
import csv, re, time, math

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
level=logging.WARNING) 


Filter = {'music':InputMessagesFilterMusic, 'photo':InputMessagesFilterPhotos, 'contact':InputMessagesFilterContacts,
          'url':InputMessagesFilterUrl, 'video':InputMessagesFilterVideo, 'document':InputMessagesFilterDocument}

class client:
    def __init__(self, session, api_id, api_hash):
        self.client = TelegramClient(session, api_id, api_hash)
        self.client.start()

    def scrape(self, chat, from_peer, limit, filter, offset_date=datetime.now()): #set limit under 2000 to avoid hitting flood wait
        global Filter
        chat_entity = self.client.get_entity(chat)
        from_peer_entity = self.client.get_entity(from_peer)
        
        for i in range(math.ceil(limit/100)):
            try: 
                total = self.client.get_messages(from_peer_entity, limit=100, offset_date=offset_date, filter=Filter[filter])
                self.client.forward_messages(chat_entity, total)
                print(total[-1].date)
            except FloodWaitError as e:
                print(e)
                wait_time = int(re.findall('\d+',str(e))[0])
                time.sleep(wait_time)
                continue

        
   

