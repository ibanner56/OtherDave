import unittest
from otherdave.commands import haiku

class HaikuTestCase(unittest.TestCase):
    def setUp(self):
        haiku.masterSyllables.set("haiku", 2)
        haiku.masterSyllables.set("many", 2)

    def tearDown(self):
        haiku.flushCache()
        haiku.memories.deldb()

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

class DebugHaikuTestCase(unittest.TestCase):
    def setUp(self):
        haiku.masterSyllables.set("haiku", 2)

    def tearDown(self):
        haiku.flushCache()
        haiku.memories.deldb()

    def test_debug(self):
        self.assertEqual(haiku.debug("Spork test"), "Spork - 1\ntest - 2\n")

    def test_debuglast(self):
        text = "This one is a test. This poem is a haiku. Refrigerator."
        expected = "This - 1\none - 2\nis - 3\na - 4\ntest. - 5\nThis - 6\npoem - 8\nis - 9\na - 10\nhaiku. - 12\nRefrigerator. - 17\n"
        self.assertIsNotNone(haiku.parseHaiku(text, False))
        self.assertEqual(haiku.debug(""), expected)

class CorrectHaikuTestCase(unittest.TestCase):
    def setUp(self):
        haiku.masterSyllables.set("haiku", 2)

    def tearDown(self):
        haiku.flushCache()
        haiku.memories.deldb()

    def test_correct(self):
        self.assertTrue(haiku.correct("spork", "5"))
        self.assertIsNotNone(haiku.parseHaiku("spork test spork test spork", False))
        self.assertTrue(haiku.correct("spork", "1"))
    
    def test_badcorrect(self):
        self.assertFalse(haiku.correct("spoon", "fork"))


class SaveHaikuTestCase(unittest.TestCase):
    def setUp(self):
        haiku.masterSyllables.set("haiku", 2)

    def tearDown(self):
        haiku.flushCache()
        haiku.memories.deldb()

    def test_savelast(self):
        text = "This one is a test. This poem is a haiku. Refrigerator."
        expected = "*This one is a test.*\n*This poem is a haiku.*\n*Refrigerator.*"
        self.assertIsNotNone(haiku.parseHaiku(text, False))
        self.assertEqual(haiku.save(""), haiku._savedHaiku)
        self.assertEqual(haiku.recall(), expected)

    def test_savewithkeywords(self):
        text1 = "This one is a test. This poem is a haiku. Refrigerator."
        text2 = "This too is a test. This poem is a haiku. Refrigerator."
        expected = "*This one is a test.*\n*This poem is a haiku.*\n*Refrigerator.*"
        self.assertIsNotNone(haiku.parseHaiku(text1, False))
        self.assertIsNotNone(haiku.parseHaiku(text2, False))
        self.assertEqual(haiku.save("This one"), haiku._savedHaiku)
        self.assertEqual(haiku.recall(), expected)

    def test_savewithbadkeywords(self):
        text = "This one is a test. This poem is a haiku. Refrigerator."
        self.assertIsNotNone(haiku.parseHaiku(text, False))
        self.assertEqual(haiku.save("Farts"), haiku._badKeywords)

    def test_recallemptymemory(self):
        self.assertEqual(haiku.recall(), haiku._emptyMemory)

    def test_saveemptybuffer(self):
        self.assertEqual(haiku.save(""), haiku._emptyBuffer)

class ForgetHaikuTestCase(unittest.TestCase):
    def setUp(self):
        haiku.masterSyllables.set("haiku", 2)

    def tearDown(self):
        haiku.flushCache()
        haiku.memories.deldb()

    def test_forgetemptybuffer(self):
        self.assertEqual(haiku.forget(""), haiku._emptyBuffer)

    def test_forgetlast(self):
        text = "This one is a test. This poem is a haiku. Refrigerator."
        expected = "*This one is a test.*\n*This poem is a haiku.*\n*Refrigerator.*"
        self.assertIsNotNone(haiku.parseHaiku(text, False))
        self.assertEqual(haiku.save(""), haiku._savedHaiku)
        self.assertEqual(haiku.recall(), expected)
        self.assertEqual(haiku.forget(""), haiku._forgetSuccess)

    def test_forgetwithkeywords(self):
        text1 = "This one is a test. This poem is a haiku. Refrigerator."
        text2 = "This too is a test. This poem is a haiku. Refrigerator."
        expected = "*This one is a test.*\n*This poem is a haiku.*\n*Refrigerator.*"
        self.assertIsNotNone(haiku.parseHaiku(text1, False))
        self.assertIsNotNone(haiku.parseHaiku(text2, False))
        self.assertEqual(haiku.save("This one"), haiku._savedHaiku)
        self.assertEqual(haiku.recall(), expected)
        self.assertEqual(haiku.forget("This one"), haiku._forgetSuccess)

    def test_forgetwithbadkeywords(self):
        text1 = "This one is a test. This poem is a haiku. Refrigerator."
        text2 = "This too is a test. This poem is a haiku. Refrigerator."
        expected = "*This one is a test.*\n*This poem is a haiku.*\n*Refrigerator.*"
        self.assertIsNotNone(haiku.parseHaiku(text1, False))
        self.assertIsNotNone(haiku.parseHaiku(text2, False))
        self.assertEqual(haiku.save("This one"), haiku._savedHaiku)
        self.assertEqual(haiku.recall(), expected)
        self.assertEqual(haiku.forget("Farts"), haiku._badKeywords)