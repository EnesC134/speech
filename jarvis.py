from jarvis_ausgabe import Jarvis_Ausgabe
from jarvis_bot import Jarvis_ChatBot

import os, sys, struct
from icecream import ic
import pvporcupine
import os

#import wave
from datetime import datetime

from vosk import Model, KaldiRecognizer
import json
import pyaudio

import wikipedia



sys.path.append(os.path.join(os.path.dirname(__file__), '/home/andy/Dokumente/workspace/porcupine/binding/python'))
sys.path.append(os.path.join(os.path.dirname(__file__), '/home/andy/Dokumente/workspace/porcupine/resources/util/python'))


            
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
    jarvis_ausgabe =Jarvis_Ausgabe(konsole=True, sprache=False)
    chat=Jarvis_ChatBot(language='de', ausgabe=jarvis_ausgabe)
    
    #model = Model ('sprachmodelle/vosk-model-de-0.21')      # Großes Model mit 1,4 GB
    model = Model ('sprachmodelle/vosk-model-small-de-zamia-0.3') #kleines Model mit 50MB
    
    recognizer:KaldiRecognizer = KaldiRecognizer(model, 16000)
    pa:pyaudio = None        
    wakewords:list[str]=check_wakeword_list(wakewords)
    
  

    
    
    
    try:
        porcupine = pvporcupine.create(
            access_key=access_key, 
            keywords=wakewords
        )

        print('Porcupine version: %s' % porcupine.version)
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate, 
            channels=1, 
            format=pyaudio.paInt16, 
            input=True, 
            frames_per_buffer=porcupine.frame_length,
            input_device_index=-1)
        
        jarvis_ausgabe.ausgabe("Hallo, ich bin Jarvis. Wie kann ich Ihnen helfen?") 
        print('Listening for keywords ' + ', '.join(wakewords) + '. Press Ctrl+C to exit.')
    
        is_listening = False
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)    
            
            result = porcupine.process(pcm_unpacked)
           
            if result >= 0:
                is_listening = True
                print('[%s] Detected %s' % (str(datetime.now()), wakewords[result]))

            if is_listening:
                if recognizer.AcceptWaveform(pcm):
                    result = json.loads(recognizer.Result())
                    ic ("Ich habe verstanden: "+ result["text"])
                    is_listening = False
                                        
                    jarvis_ausgabe.ausgabe(chat.conversation(result['text']))
                                        
                    print('Listening for keywords ' + ', '.join(wakewords) + '. Press Ctrl+C to exit.')
    
    
    
    
    except KeyboardInterrupt:
        print('stopping...')
    finally:
        if porcupine is not None:
            print("delete porcupine instance")
            porcupine.delete()
            
        if audio_stream is not None:
            print("close audio stream")
            audio_stream.close()
        
        if pa is not None:
            print("terminate pyaudio")
            pa.terminate()
        



def check_wakeword_list(wakewords:list[str])->list[str]:
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
    allowed_wakewords:list[str] = list(pvporcupine.KEYWORDS)
    my_wakewords:list[str]=[]
    
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

    