import unittest


class TestHelloWorld(unittest.TestCase):

    def test_say_hi(self):
        print('Hello World!!!')
        self.assertTrue(True)
