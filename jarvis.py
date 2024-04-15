import os, sys, struct
from icecream import ic
import pvporcupine
import os
from dotenv import load_dotenv, find_dotenv

from pvrecorder import PvRecorder
import wave
from datetime import datetime


            
def start_jarvis(access_key:str, wakewords:list=None )->None:
    """
    Startet den Jarvis Sprachassistenten.

    Parameters:
    access_key (str): Der Zugangsschlüssel für die Porcupine Spracherkennungsbibliothek.
    wakewords (list, optional): Eine Liste von "Schlüsselworten", auf die der Assistent reagieren soll. 
                                Wenn keine Liste angegeben wird, wird standardmäßig ["jarvis"] verwendet. 
                                Unabhängig von der übergebenen Liste ist "jarvis" immer ein Schlüsselwort., 
    Returns:
    None
    """
    #access_key = os.getenv('PORCUPINE_ACCESS_KEY')

    porcupine = None
    audio_stream = None
        
    wakewords=check_wakeword_list(wakewords)
    
    try:
        porcupine = pvporcupine.create(
            access_key=access_key, 
            keywords=wakewords
        )

        print('Porcupine version: %s' % porcupine.version)
        
        audio_stream = PvRecorder(
            frame_length=porcupine.frame_length,
            device_index=-1)
        audio_stream.start()

        print('Listening for keywords ' + ', '.join(wakewords) + '. Press Ctrl+C to exit.')
    
        while True:
            pcm = audio_stream.read()
            
            result = porcupine.process(pcm)
           
            if result >= 0:
                print('[%s] Detected %s' % (str(datetime.now()), wakewords[result]))

    except KeyboardInterrupt:
        print('stopping...')
    finally:
        if porcupine is not None:
            print("delete porcupine instance")
            porcupine.delete()
            
        if audio_stream is not None:
            print("close audio stream")
            audio_stream.delete()


def check_wakeword_list(wakewords:list)->list:
    """
    Überprüft die Liste der Schlüsselwörter und fügt das Standard-Schlüsselwort "jarvis" hinzu, 
    wenn es nicht in der Liste enthalten ist.

    Parameters:
    wakewords (list): Eine Liste von "Schlüsselworten", auf die der Assistent reagieren soll. 
                      Wenn keine Liste angegeben wird, wird standardmäßig ["jarvis"] verwendet. 
                      Unabhängig von der übergebenen Liste ist "jarvis" immer ein Schlüsselwort., 

    Returns:
    list: Eine Liste von "Schlüsselworten", auf die der Assistent reagieren soll. 
    """
    allowed_wakewords:list = list(pvporcupine.KEYWORDS)
    my_wakewords:list=[]
    
    for word in wakewords:
        if word not in allowed_wakewords:
            print(f"'{word}' ist kein erlaubtes Schlüsselwort. Es wird ignoriert.")
        else:
            my_wakewords.append(word)
            
    if "jarvis" not in my_wakewords:
        my_wakewords.append("jarvis")
    
    return my_wakewords
           

if __name__ == "__main__":
    start_jarvis(access_key=os.getenv('PORCUPINE_ACCESS_KEY'), wakewords=["picovoice","alexa", "terminator","blub"])

    