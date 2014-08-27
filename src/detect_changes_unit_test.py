#!/usr/bin/env python
""" This script is used to unit test the detect_changes script."""

# pylint: disable=W0403
import unittest
import detect_changes
import logging
from datetime import datetime
import os


class detectChangesUnitTest(unittest.TestCase):
    """This class is used for unit testing detect_changes.py script.
    """
    def setUp(self):
        """ Sets up variables for unit testing.
        """
        self.find_changes = detect_changes.detectChanges("need_a_file") # change this line

    def test_01_get_timestamp_success(self):
        """ Test the success case of get_timestamp function."""
        file_name = "./test_data/changedtime"
        status, timestamp = self.find_changes.get_last_changed_time(file_name)
        self.assertTrue(status)
        assert timestamp > 0, "time stamp validation failed"

    def test_02_get_timestamp_failure(self):
        """Test the failure case of get_timestamp function."""
        file_name = "not_a_file"
        status, timestamp = self.find_changes.get_last_changed_time(file_name)
        self.assertFalse(status)
        self.assertEquals(timestamp, 0)


if __name__ == "__main__":
    LOG_DIR = "/var/log/replication/"
    LOG_BASE_FILE = "detect_changes_unit_test_"
    LOG_FILE = "".join([LOG_DIR, LOG_BASE_FILE,
                        datetime.now().strftime("%Y%m%d_%H%M%S_%f"), ".log"])
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    open(LOG_FILE, 'a').close() # create log file if not present
    print "log file is ", LOG_FILE
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    unittest.main() 
