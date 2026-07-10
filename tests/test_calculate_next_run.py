import unittest
from unittest.mock import patch
from datetime import datetime
from src.utils.calculate_next_run import calculate_interval, calculate_date_time

class TestCalculateNextRun(unittest.TestCase):

    @patch("src.utils.calculate_next_run.datetime")
    def test_calculate_interval_days(self, mock_datetime):
        fixed_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now

        result = calculate_interval("days", 3)

        assert result == datetime(2025, 1, 4, 12, 0, 0)

    @patch("src.utils.calculate_next_run.datetime")
    def test_calculate_interval_hours(self, mock_datetime):
        fixed_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now

        result = calculate_interval("hours", 3)

        assert result == datetime(2025, 1, 1, 15, 0, 0)
        
    @patch("src.utils.calculate_next_run.datetime")
    def test_calculate_interval_min(self, mock_datetime):
        fixed_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now

        result = calculate_interval("minutes", 30)

        assert result == datetime(2025, 1, 1, 12, 30, 0)

    @patch("src.utils.calculate_next_run.datetime")
    def test_calculate_interval_sec(self, mock_datetime):
        fixed_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now

        result = calculate_interval("seconds", 90)

        assert result == datetime(2025, 1, 1, 12, 1, 30)

    @patch("src.utils.calculate_next_run.datetime")
    def test_calculate_date_time_current_month(self, mock_datetime):
        fixed_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = datetime
        mock_datetime.strptime.side_effect = datetime.strptime

        result = calculate_date_time("06:00", 5)

        assert result == datetime(2025, 1, 5, 6, 0, 0)

    @patch("src.utils.calculate_next_run.datetime")
    def test_calculate_date_time_next_month(self, mock_datetime):
        fixed_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = datetime
        mock_datetime.strptime.side_effect = datetime.strptime

        result = calculate_date_time("06:00", 1)

        assert result == datetime(2025, 2, 1, 6, 0, 0)

    @patch("src.utils.calculate_next_run.datetime")
    def test_calculate_date_time_day_not_in_month(self, mock_datetime):
        fixed_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = datetime
        mock_datetime.strptime.side_effect = datetime.strptime

        result = calculate_date_time("06:00", 60)

        assert result == datetime(2025, 1, 31, 6, 0, 0)

    

if __name__ == "__main__":
    unittest.main()