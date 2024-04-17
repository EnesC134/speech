import os, sys, struct
from icecream import ic
import pvporcupine
import os
from dotenv import load_dotenv, find_dotenv

from pvrecorder import PvRecorder
import wave
from datetime import datetime

from vosk import Model, KaldiRecognizer
import json
import pyaudio

from chatbot import Chat, register_call

import wikipedia

import pyttsx3

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
    
    model = Model ('sprachmodelle/vosk-model-de-0.21')      # Großes Model mit 1,4 GB
    #model = Model ('sprachmodelle/vosk-model-small-de-zamia-0.3') #kleines Model mit 50MB
    
    recognizer:KaldiRecognizer = KaldiRecognizer(model, 16000)
    pa:pyaudio = None        
    wakewords:list[str]=check_wakeword_list(wakewords)
    
    
    MAIN_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    DIALOG_TEMPLATE =MAIN_FILE_DIR + '/chat_dialog/dialog.template'
    ic("DIALOG_TEMPLATE: ", DIALOG_TEMPLATE)

    chat=Chat(DIALOG_TEMPLATE)
    
    wikipedia.set_lang("de")
    
    tts=pyttsx3.init()
    voices = tts.getProperty('voices')
    #for v in voices:
    #    print (v.id)
    tts.setProperty('voice', 'german')
    tts.say ("Hallo, ich bin Jarvis. Wie kann ich Ihnen helfen?")
    tts.runAndWait()
        
    @register_call("wasIst")
    def who_is(session, query:str):
        """
        TEIL DES CHATBOTS

        Args:
            session (_type_): _description_
            query (str): _description_

        Returns:
            _type_: _description_
        """
        ic ("Call wasIst was called with query: ",query)
        
        try:
            return wikipedia.summary(query, sentences=1)
        
        except Exception:
            for new_query in wikipedia.search(query):
                try:
                    return wikipedia.summary(new_query, sentences=1)
                except Exception:
                    print ("Konnte keine Infos finden.")
        
        ic ("Can't answer to ", query)    
        
    def conv(input:str)->bool:
        """
        TEIL DES CHATBOTS
        nimmt die chatanfrage entgegen

        Args:
            input (str): die Anfrage vom Benutzer an den chatbot

        Returns:
            bool: immer False, weil das in Jarvis benötigt wird um das is_listen zu beenden.
        """
        output = chat.respond(input)
        print (output)
        tts.say(output)
        tts.runAndWait()
        return False
    
    
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
        
        print('Listening for keywords ' + ', '.join(wakewords) + '. Press Ctrl+C to exit.')
    
        is_lisetening = False
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)    
            
            result = porcupine.process(pcm_unpacked)
           
            if result >= 0:
                is_lisetening = True
                print('[%s] Detected %s' % (str(datetime.now()), wakewords[result]))

            if is_lisetening:
                if recognizer.AcceptWaveform(pcm):
                    result = json.loads(recognizer.Result())
                    ic ("Ich habe verstanden: "+ result["text"])
                    is_lisetening = conv(result['text'])
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

    