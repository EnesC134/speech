from jarvis import start_jarvis
from dotenv import load_dotenv
import os

from icecream import ic

if __name__ == '__main__':
    load_dotenv('./env/no_git_porcupine_key.env')
    key =None
    key = os.getenv('PORCUPINE_KEY')   
    
    if key is not None:
        start_jarvis(ACCESS_KEY=key, wakewords=["picovoice","alexa", "terminator","blub"])