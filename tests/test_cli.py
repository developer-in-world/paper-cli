import unittest
from pathlib import Path
import tempfile
import os

class TestStorageModule(unittest.TestCase):
    def setUp(self):
        # Override the DB_FILE in the module to a temp file
        self.temp_db_path = Path(tempfile.mktemp())
        import storage
        storage.DB_FILE = self.temp_db_path
        storage.init_db()

    def tearDown(self):
        if self.temp_db_path.exists():
            self.temp_db_path.unlink()

    def test_save_and_retrieve_paper(self):
        import storage
        paper = {"title": "Test Paper", "authors": ["Alice"], "url": "http://arxiv/1"}
        repo = {"url": "http://github.com/alice/test", "stars": 500}
        
        storage.save_paper(paper, repo, "Great summary", ["test_tag"])
        
        results = storage.search_saved_papers("Test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Test Paper")
        self.assertEqual(results[0]["github_stars"], 500)
        self.assertEqual(results[0]["tags"], "test_tag")
        
    def test_search_empty_database(self):
        import storage
        results = storage.search_saved_papers("Nonexistent")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
