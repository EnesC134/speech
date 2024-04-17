import os, sys
from chatbot import Chat, register_call
from icecream import ic
from jarvis_ausgabe import Jarvis_Ausgabe

#Imports für Chat-Funktionen
import wikipedia
sys.path.append('/home/andy/Dokumente/workspace/')
sys.path.append('/home/andy/Dokumente/workspace/FOS_Praktikumsberichte')
from FOS_Praktikumsberichte import main as berichte

# Der Chatbot ist zu finden auf:
# https://github.com/ahmadfaizalbh/Chatbot/


class Jarvis_ChatBot(Chat):
    """
    Eine Wrapper-Klasse für den Chatbot, die von der ChatBot-Klasse erbt.
    """

    def __init__(self,ausgabe:Jarvis_Ausgabe, *args, **kwargs):
        """
        Initialisiert den Wrapper und ruft den Konstruktor der übergeordneten Klasse auf.

        :param name: Der Name des Chatbots.
        """
        self.MAIN_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.DIALOG_TEMPLATE = self.MAIN_FILE_DIR + '/chat_dialog/dialog.template'
        self.jarvis_ausgabe = ausgabe
        ic("DIALOG_TEMPLATE: ", self.DIALOG_TEMPLATE)
        super().__init__(self.DIALOG_TEMPLATE, *args, **kwargs)
    
    def conversation(self, input:str) -> str:
        """
        Führt eine Konversation mit dem Chatbot durch und gibt die Antwort zurück.

        :param input: Die Eingabe für den Chatbot.
        :return: Die Antwort des Chatbots auf die Eingabe.
        """
        return self.respond(input)

    ############################################
    ###
    ### Chatbot Funktionen
    ###
    ############################################

       
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
        wikipedia.set_lang("de")
        return wikipedia.summary(query, sentences=1)
    
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query, sentences=1)
            except Exception:
                self.jarvis_ausgabe.ausgabe ("Konnte keine Infos finden.")
    
    ic ("Can't answer to ", query)    

@register_call("Praktikumsberichte")
def praktikumsberichte(session, query:str):
    ic ("Praktiumsberichte was called.")
    berichte.main()
    return "Praktikumsberichte werden geladen. Bitte warten."
    