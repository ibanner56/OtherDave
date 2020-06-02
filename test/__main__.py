# otherdave/test/__main__.py

import sys
import unittest

sys.path.append("../commands")

loader = unittest.TestLoader()
testSuite = loader.discover("test")
testRunner = unittest.TextTestRunner(verbosity=2)
testRunner.run(testSuite)