import unittest
from models import *


class ResponseTest(unittest.TestCase):

    def setUp(self):
        self.response = Response("Test answer", "training", 1, 1)

    def tearDown(self):
        del self.response

    def test_response_is_a_response_object(self):
        self.assertIsInstance(self.response, Response)

    def test_response_has_answer(self):
        self.assertEqual(self.response.answer, "Test answer")

    def test_response_has_role(self):
        self.assertEqual(self.response.role, "training")

    def test_response_has_categories_id(self):
        self.assertEqual(self.response.categories_id, 1)

    def test_response_has_questions_id(self):
        self.assertEqual(self.response.questions_id, 1)

    def test_response_has_classifier(self):
        print(self.response.classify_response)
        self.assertIsNot(self.response.classify_response, None)

if __name__ == '__main__':
    unittest.main()
