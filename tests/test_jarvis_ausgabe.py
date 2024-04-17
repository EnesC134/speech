import unittest
from unittest.mock import patch
from jarvis_ausgabe import Jarvis_ausgabe

class TestJarvisAusgabe(unittest.TestCase):
    def setUp(self):
        self.jarvis = Jarvis_ausgabe()

    @patch('builtins.print')
    def test_ausgabe_konsole(self, mock_print):
        self.jarvis.konsole = True
        self.jarvis.ausgabe("Hallo")
        mock_print.assert_called_once_with("Hallo")

    def test_ausgabe_sprache(self):
        self.jarvis.sprache = True
        with self.assertRaises(NotImplementedError):
            self.jarvis.ausgabe("Hallo")
    
    def test_set_sprache(self):
        self.jarvis.set_sprache(True)
        self.assertEqual(self.jarvis.sprache, True)
        self.jarvis.set_sprache(False)
        self.assertEqual(self.jarvis.sprache, False)

    def test_set_konsole(self):
        self.jarvis.set_konsole(True)
        self.assertEqual(self.jarvis.konsole, True)
        self.jarvis.set_konsole(False)
        self.assertEqual(self.jarvis.konsole, False)

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()