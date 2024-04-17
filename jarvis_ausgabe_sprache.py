import pyttsx3

class Jarvis_Sprachausgabe:
    """
    Eine Klasse, die die Sprachausgabe für Jarvis bereitstellt.
    """

    def __init__(self):
        """
        Initialisiert die Text-zu-Sprache-Engine und setzt die Stimme auf Deutsch.
        """
        self.tts = pyttsx3.init()  
        self.tts.setProperty('voice', 'german')  

    def get_all_voices(self) -> None:
        """
        Gibt alle verfügbaren Stimmen aus.
        """
        voices = self.tts.getProperty('voices')  
        for v in voices:
            print(v.id)  

    def ausgabe(self, text: str) -> None:
        """
        Liest den gegebenen Text laut vor.

        :param text: Der Text, der vorgelesen werden soll.
        """
        self.tts.say(text)  
        self.tts.runAndWait()  
