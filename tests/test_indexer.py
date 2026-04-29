import unittest
import os
import sys
import shutil

# Add src to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from indexer import QuoteIndexer

class TestQuoteIndexer(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = "test_data"
        self.indexer = QuoteIndexer(data_dir=self.test_data_dir)
        self.sample_quotes = [
            {
                "text": "The world is what it is.",
                "author": "V.S. Naipaul",
                "tags": "life, reality",
                "url": "http://example.com/1"
            },
            {
                "text": "Life is a journey.",
                "author": "Unknown",
                "tags": "life, travel",
                "url": "http://example.com/2"
            }
        ]

    def tearDown(self):
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)

    def test_build_index(self):
        self.indexer.build_index(self.sample_quotes)
        # "life" should be in both documents
        self.assertIn("life", self.indexer.index)
        self.assertEqual(len(self.indexer.index["life"]), 2)
        # "journey" should be in doc 1 (0-indexed)
        self.assertIn("journey", self.indexer.index)
        self.assertIn(1, self.indexer.index["journey"])

    def test_save_and_load(self):
        self.indexer.build_index(self.sample_quotes)
        self.indexer.save_index()
        
        new_indexer = QuoteIndexer(data_dir=self.test_data_dir)
        new_indexer.load_index()
        
        self.assertEqual(len(new_indexer.documents), 2)
        self.assertEqual(new_indexer.index["life"], self.indexer.index["life"])

if __name__ == '__main__':
    unittest.main()
