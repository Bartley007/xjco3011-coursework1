import unittest
import os
import sys

# Add src to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from search import QuoteSearcher

class TestQuoteSearcher(unittest.TestCase):
    def setUp(self):
        self.index = {
            "life": {"0": [0], "1": [0]},
            "journey": {"1": [2]},
            "world": {"0": [1]}
        }
        self.documents = [
            {"text": "Life world", "author": "A", "tags": "T1", "url": "U1"},
            {"text": "Life is journey", "author": "B", "tags": "T2", "url": "U2"}
        ]
        self.searcher = QuoteSearcher(self.index, self.documents)

    def test_find_single_word(self):
        results = self.searcher.find(["life"])
        self.assertEqual(len(results), 2)

    def test_find_multiple_words(self):
        # Intersection of "life" and "journey" should be doc 1
        results = self.searcher.find(["life", "journey"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["author"], "B")

    def test_find_no_match(self):
        results = self.searcher.find(["nonexistent"])
        self.assertEqual(len(results), 0)

    def test_find_empty_query(self):
        results = self.searcher.find([])
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
