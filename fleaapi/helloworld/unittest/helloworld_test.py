from django.test import TestCase
from unittest.mock import MagicMock


from ..helloworld import *


class HelloWorldTest(TestCase):
    def setUp(self) -> None:
        self.request = MagicMock()
        self.request.method = "GET"

    def test_helloworld(self):
        self.assertJSONEqual(
            helloworld(self.request).content, {"message": "Hello, world!"}
        )







       
