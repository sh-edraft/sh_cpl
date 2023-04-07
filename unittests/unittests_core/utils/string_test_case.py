import string
import unittest

from cpl_core.utils import String


class StringTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_convert_to_camel_case(self):
        expected = "HelloWorld"

        self.assertEqual(expected, String.convert_to_camel_case("hello-world"))
        self.assertEqual(expected, String.convert_to_camel_case("hello_world"))
        self.assertEqual("helloWorld", String.convert_to_camel_case("helloWorld"))
        self.assertEqual(expected, String.convert_to_camel_case("Hello_world"))
        self.assertEqual(expected, String.convert_to_camel_case("Hello_World"))
        self.assertEqual(expected, String.convert_to_camel_case("hello world"))

    def test_convert_to_snake_case(self):
        expected = "hello_world"

        self.assertEqual(expected, String.convert_to_snake_case("Hello World"))
        self.assertEqual(expected, String.convert_to_snake_case("hello-world"))
        self.assertEqual(expected, String.convert_to_snake_case("hello_world"))
        self.assertEqual(expected, String.convert_to_snake_case("helloWorld"))
        self.assertEqual(expected, String.convert_to_snake_case("Hello_world"))
        self.assertEqual(expected, String.convert_to_snake_case("Hello_World"))
        self.assertEqual(expected, String.convert_to_snake_case("hello world"))

    def test_first_to_upper(self):
        expected = "HelloWorld"

        self.assertEqual(expected, String.first_to_upper("helloWorld"))
        self.assertEqual(expected, String.first_to_upper("HelloWorld"))

    def test_first_to_lower(self):
        expected = "helloWorld"

        self.assertEqual(expected, String.first_to_lower("helloWorld"))
        self.assertEqual(expected, String.first_to_lower("HelloWorld"))

    def test_random_string(self):
        expected = ""

        for x in range(0, 100):
            rstr = String.random_string(string.ascii_letters, 4)
            self.assertNotEqual(expected, rstr)
            self.assertEqual(4, len(rstr))
            expected = rstr

        for x in range(0, 100):
            rstr = String.random_string(string.ascii_letters, 16)
            self.assertNotEqual(expected, rstr)
            self.assertEqual(16, len(rstr))
            expected = rstr
