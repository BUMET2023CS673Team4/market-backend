from io import StringIO
import re
from django.core.management import call_command
from django.test import TestCase


class FillRandomDataTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command("fill_random_data", stdout=out)
        outlines = out.getvalue().splitlines()
        self.assertEqual(len(outlines), 4)
        self.assertTrue(re.match(r"Created \d+ users", outlines[0]))
        self.assertTrue(re.match(r"Created \d+ seller profiles", outlines[1]))
        self.assertTrue(re.match(r"Created \d+ categories", outlines[2]))
        self.assertTrue(re.match(r"Created \d+ items", outlines[3]))
