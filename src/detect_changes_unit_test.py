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
        self.find_changes = detect_changes.\
            detectChanges("./test_data/config_data")

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

    def test_03_get_previous_changed_time(self):
        """Test the get_previous_changed_time function."""
        timestamp = self.find_changes.get_previous_changed_time()
        self.assertEquals(timestamp, 1409237071)

    def test_04_get_log_file(self):
        """Test the get log file function."""
        log_file = self.find_changes.get_log_file()
        self.assertEquals(log_file, "/var/log/mysql/mysql-bin.000002")

    def test_05_get_previous_index_pos(self):
        """Test the get previous index position function."""
        index_pos = self.find_changes.get_previous_index_pos()
        self.assertEquals(index_pos, 1200)

    def test_06_get_index_file(self):
        """Test the get_index_file function."""
        index_file = self.find_changes.get_index_file()
        self.assertEquals(index_file, "/var/log/mysql/mysql-bin.index")

    def test_07_merge_config_protobuf(self):
        """Test the success stae of merge config protobuf function."""
        self.assertTrue(self.find_changes.merge_config_protobuf())

    def test_08_merge_config_failure(self):
        """Test the failure cases of merge config protobuf function."""
        self.find_changes.lookup_file = None
        self.assertFalse(self.find_changes.merge_config_protobuf())

        self.find_changes.lookup_file = 'Not_a_file'
        self.assertFalse(self.find_changes.merge_config_protobuf())

        self.find_changes.lookup_file = './test_data/invalid_format_proto'
        self.assertFalse(self.find_changes.merge_config_protobuf())

    def test_09_check_changes_success(self):
        """ Test the success cases of check changes function."""
        self.find_changes.lookup_file = './test_data/proper_config_data'
        status, changes = self.find_changes.check_changes()
        self.assertTrue(status)
        self.assertEquals(changes, 'Yes')

        logging.info("Calling check changes function for nochanges case.")
        self.find_changes.lookup_file = './test_data/no_changes_config_data'
        status, changes = self.find_changes.check_changes()
        self.assertTrue(status)
        self.assertEquals(changes, 'No')

    def test_10_check_changes_failure(self):
        """Test the failure cases of check changes function."""
        self.find_changes.lookup_file = 'not_a_file'
        status, changes = self.find_changes.check_changes()
        self.assertFalse(status)
        self.assertEquals(changes, 'No')

        self.find_changes.replication_details.log_file = 'not_a_file'
        status, changes = self.find_changes.check_changes()
        self.assertFalse(status)
        self.assertEquals(changes, 'No')

        self.find_changes.replication_details.log_file = './test_data/changedtime'
        self.find_changes.replication_details.index_file = 'not_a_file'
        status, changes = self.find_changes.check_changes()
        self.assertFalse(status)
        self.assertEquals(changes, 'No')

    def tearDown(self):
        """Cleans up the objects after each test case."""
        self.find_changes = None

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
