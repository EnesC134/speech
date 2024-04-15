import unittest
from jarvis import check_wakeword_list

class TestCheckWakewordList(unittest.TestCase):
    def test_check_wakeword_list(self):
        # Test, ob "jarvis" hinzugefügt wird, wenn es nicht in der Liste ist
        wakewords = ["alexa", "hey google"]
        result = check_wakeword_list(wakewords)
        self.assertIn("jarvis", result)

        # Test, ob nicht erlaubte Wörter ignoriert werden
        wakewords = ["alexa", "not_allowed"]
        result = check_wakeword_list(wakewords)
        self.assertNotIn("not_allowed", result)

if __name__ == '__main__':
    unittest.main()