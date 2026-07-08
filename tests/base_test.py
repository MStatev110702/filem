import unittest
from src.entry import Entry

class BaseTest(unittest.TestCase):
    def create_test_entry(self, **overrides) -> Entry:
        data = {
            "id": None,
            "name": "test",
            "description": "test123",
            "type": "COPY",
            "interval_type": "manually",
            "schedule_type": "",
            "schedule_value": 0,
            "originpath": "/origintmp",
            "destpath": "/desttmp",
            "include_dir": "none",
            "include_files": "none"
        }

        data.update(overrides)
        return Entry(**data)
    

if __name__ == "__main__":
    unittest.main()