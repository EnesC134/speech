from jarvis import start_jarvis
import os

if __name__ == '__main__':
    start_jarvis(access_key=os.getenv('PORCUPINE_ACCESS_KEY'), wakewords=["picovoice","alexa", "terminator","blub"])