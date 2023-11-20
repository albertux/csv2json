# test_main.py

import unittest
from unittest.mock import patch
import argparse
import sys
import json
from io import StringIO
from csv2json import main

class TestMyScript(unittest.TestCase):

    maxDiff = None

    def test_wiki_good(self):

# json output generated using: jq . -r test/wiki.json
        json_output="""
[
  {
    "Year": "1997",
    "Make": "Ford",
    "Model": "E350",
    "Description": "ac; abs; moon",
    "Price": "3000.00"
  },
  {
    "Year": "1999",
    "Make": "Chevy",
    "Model": "Venture Extended Edition",
    "Description": "",
    "Price": "4900.00"
  },
  {
    "Year": "1999",
    "Make": "Chevy",
    "Model": "Venture Extended Edition; Very Large",
    "Description": "",
    "Price": "5000.00"
  }
]
"""
        test_args = ['-f', 'test/wiki.csv', '-o', 'test/wiki.json', '-w', '-p']
        with patch.object(sys, 'argv', ['cvs2json'] + test_args), patch('sys.stdout', new=StringIO()) as fake_output:
            main()
            output = fake_output.getvalue()
            self.assertEqual(output.split(), json_output.split())

    def test_wiki_bad(self):
        test_args = ['-f', 'test/wiki-bad.csv', '-o', 'test/wiki-bad.json']
        with patch.object(sys, 'argv', ['cvs2json'] + test_args), patch('sys.stderr', new=StringIO()) as fake_stderr:
            with self.assertRaises(SystemExit) as cm:
                main()
                output = fake_stderr.getvalue().strip()
                self.assertEqual(output, f"file examples/wiki-bad.csv, line 5: number of fields does not match previous line")
                self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
