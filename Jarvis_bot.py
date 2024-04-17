import os
from chatbot import Chat, register_call
from icecream import ic

def dummy():
    MAIN_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    DIALOG_TEMPLATE =MAIN_FILE_DIR + '/chat_dialog/dialog.template'
    ic("DIALOG_TEMPLATE: ", DIALOG_TEMPLATE)

    chat=Chat(DIALOG_TEMPLATE)

@register_call("wasIst")
def who_is(query,session_id="general"):
    ic ("Call wasIst was called with query: "+ query)
    
    try:
        return "Got query!"
    except Exception:
        pass
    
    ic ("Can't answer to ", query)

def conv(input):
    output = chat.respond(input)
    return False