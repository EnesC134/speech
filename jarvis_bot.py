import os
from chatbot import Chat, register_call
from icecream import ic

#Imports für Chat-Funktionen
import wikipedia

# Der Chatbot ist zu finden auf:
# https://github.com/ahmadfaizalbh/Chatbot/


class Jarvis_ChatBot(Chat):
    """
    Eine Wrapper-Klasse für den Chatbot, die von der ChatBot-Klasse erbt.
    """

    def __init__(self):
        """
        Initialisiert den Wrapper und ruft den Konstruktor der übergeordneten Klasse auf.

        :param name: Der Name des Chatbots.
        """
        self.MAIN_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.DIALOG_TEMPLATE = self.MAIN_FILE_DIR + '/chat_dialog/dialog.template'
        ic("DIALOG_TEMPLATE: ", self.DIALOG_TEMPLATE)
        super().__init__(self.DIALOG_TEMPLATE)

    
    
    
    def conv(self, input:str, consol_out:bool=True, speech_out:bool=True) -> bool:
        """
        Führt eine Konversation mit dem Chatbot durch.

        :param input: Die Eingabe für den Chatbot.
        :param consol_out: Gibt an, ob die Ausgabe in der Konsole angezeigt werden soll.
        :param speech_out: Gibt an, ob die Ausgabe als Sprachausgabe ausgegeben werden soll.
        :return: False
        """
        output = self.get_response(input)
    
        if consol_out:
            print(output)
    
        if speech_out:
            # Aufruf für Sprachausgabe
            raise NotImplementedError("Speech aufruf in \"Jarvis_bot.conf\" ist noch nicht implementiert.")

        return False

############################################
###
### Chatbot Funktionen
###
############################################

@register_call("wasIst")
def search_wikipedia(session, query:str):
    ic ("Call \"search_wikipedia\" was called with query: ",query)
    
    try:
        return wikipedia.summary(query)
    
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                print ("Konnte keine Infos finden.")
    
    ic ("Can't answer to ", query)  
