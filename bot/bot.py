from discord import Intents, Client, Message, File
from downloader.downloader import proccess_video_request
import os
import re
import json


providers_json_path = os.path.join(os.path.dirname(__file__), '..','providers.json')

with open(providers_json_path, 'r') as json_file:
    providers = json.load(json_file)['providers']
    


intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


def is_link(user_input:str):
    
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    url_match = url_pattern.search(user_input)
    
    if url_match:
        link = url_match.group(0)
        return link
    else:
        return None
    
def is_in_list(url:str) -> bool:
    print(providers)
    return any(domain in url for domain in providers)
 

        
def handle_received_message(user_message):
     link = is_link(user_message)
     
     if not link or not is_in_list(link):
         return None
     else:
        return proccess_video_request(link)
    

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

@client.event
async def on_message(message: Message) -> None: 
    if message.author == client.user: 
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    
    print(f'[{channel}] {username}: "{user_message}"')
    
    video_path = handle_received_message(user_message)
    if video_path:
        try:
            with open(video_path, 'rb') as f:
                await message.channel.send(file=File(f))
            os.remove(video_path)
            
        except Exception as e:
            print(f"An error occured\n{e}")
            

