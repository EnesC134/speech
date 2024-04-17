from jarvis_ausgabe_sprache import Jarvis_Sprachausgabe

class Jarvis_ausgabe:
    """
    Klasse für die Ausgabe von Jarvis
    """
    
    def __init__(self, konsole:bool=True, sprache:bool=True):
        """
        Konstruktor
        """
        self.konsole:bool = konsole
        self.sprache:bool = sprache
        self.sprachausgabe:Jarvis_Sprachausgabe = Jarvis_Sprachausgabe()
        

    def ausgabe(self, text:str)->None:
        """
        Methode für die Ausgabe von Jarvis. 
        Je nach Einstellung wird der Text in der Konsole ausgegeben und/oder vorgelesen.

        Args:
            text (str): der Text, der ausgegeben werden soll

        Returns:
            None
        """
        if self.konsole:
            print (text)
            
        if self.sprache:
            self.sprachausgabe.ausgabe(text)    
        
    def set_sprache(self, sprache_active:bool)->None:
        """
        Methode zum Setzen der Sprachausgabe

        Args:
            sprache (bool): True, wenn Sprachausgabe erfolgen soll, sonst False

        Returns:
            None
        """
        self.sprache = sprache_active   
        
    def set_konsole(self, konsole_active:bool)->None:
        """
        Methode zum Setzen der Konsolenausgabe

        Args:
            konsole (bool): True, wenn Konsolenausgabe erfolgen soll, sonst False

        Returns:
            None
        """
        self.konsole = konsole_active