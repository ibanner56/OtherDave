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

    def test_isempty(self):
        self.assertIsNone(haiku.parseHaiku("", False))
    
    def test_istoolong(self):
        text = "This one is a test. This poem is just too long - it has too many words."
        self.assertIsNone(haiku.parseHaiku(text, False))

    def test_withnumbers(self):
        text = "This line has 5 words, but this next line has 7 - 1005"
        self.assertIsNotNone(haiku.parseHaiku(text, False))

    def test_fermiproblem(self):
        text = "They come by the 10s... then the 100s, then more, and soon there's just 1000s"
        self.assertIsNotNone(haiku.parseHaiku(text, False))