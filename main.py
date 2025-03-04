from bot.bot import client
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def main() -> None: 
   client.run(token=TOKEN)
   
if __name__ == '__main__':
    main()