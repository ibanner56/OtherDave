import unittest
from commands import haiku

class test_haiku(unittest.TestCase):
    
    def test_ishaiku(self):
        text = "This one is a test. This poem is a haiku. Refridgerator."
        print(haiku.parseHaiku(text, True))
        self.assertIsNotNone(haiku.parseHaiku(text, False))