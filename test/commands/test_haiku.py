import unittest
from otherdave.commands import haiku

class HaikuTestCase(unittest.TestCase):
    
    def test_ishaiku(self):
        text = "This one is a test. This poem is a haiku. Refrigerator."
        self.assertIsNotNone(haiku.parseHaiku(text, False))

    def test_isnothaiku(self):
        text = "This one isn't a haiku, stupid."
        self.assertIsNone(haiku.parseHaiku(text, False))