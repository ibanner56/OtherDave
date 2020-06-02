import unittest
from otherdave.commands import haiku

class HaikuTestCase(unittest.TestCase):
    
    def test_ishaiku(self):
        text = "This one is a test. This poem is a haiku. Refrigerator."
        expected = "*This one is a test.*\n*This poem is a haiku.*\n*Refrigerator.*"
        self.assertEqual(haiku.parseHaiku(text, False), expected)

    def test_isnothaiku(self):
        text = "This one isn't a haiku, stupid."
        self.assertIsNone(haiku.parseHaiku(text, False))