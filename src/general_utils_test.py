#!/usr/bin/env python
"""This script is used to test general_utils.py script."""
# pylint:disable=R0904,W0403

import unittest
import os
import logging
from datetime import datetime
import general_utils


SUCCESS = True
FAILURE = False


class GeneralFunctionsUnitTest(unittest.TestCase):
    """ This class is used to run the different unit test on the python script
    general_utils.py.
    """
    def setUp(self):
        """ This function is used to set up environment for test cases.
        """
        logging.info(datetime.now().strftime("%Y%m%d_%H%M%S_%f") +
                     ": SETTING UP ENV\n")
        self.location = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.location)

    def test_execute_command_fail(self):
        """ Test if execute command function returns false when command fails.
        """
        logging.info("test_execute_command_fail")
        status, out = general_utils.execute_command("not a command")
        self.assertFalse(status)
        self.assertEquals(out, 'NA')

    def test_execute_command_success(self):
        """ Test if execute command function returns true when command
        succeeds.
        """
        logging.info("test_execute_command_success")
        status, ret = general_utils.execute_command("ls")
        self.assertTrue(status)

    def test_read_file_content_nofile(self):
        """ Test if read_file_contents function returns false when
        file name is not given.
        """
        logging.info("test_read_file_content_nofile")
        ret = general_utils.read_file_contents()
        self.assertFalse(ret[0])

    def test_read_file_content_fail(self):
        """ Test if read_file_contents function returns false when invalid file
        name is given.
        """
        logging.info("test_read_file_content_fail")
        ret = general_utils.read_file_contents("not_a_file")
        self.assertFalse(ret[0])

    def test_read_file_content_success(self):
        """ Test if read_file_contents function returns successfully when the
        right filename is given.
        """
        logging.info("test_read_file_content_success")
        ret = general_utils.read_file_contents("./test_data/read_file")
        self.assertTrue(ret[0])
        self.assertEquals(ret[1], 'success\n')


if __name__ == "__main__":
    LOG_DIR = "/var/log/replication/"
    LOG_BASE_FILE = "general_utils_test_"
    LOG_FILE = "".join([LOG_DIR, LOG_BASE_FILE,
                        datetime.now().strftime("%Y%m%d_%H%M%S_%f"), ".log"])
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    open(LOG_FILE, 'a').close() # create log file if not present
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    print LOG_FILE, "is log file"
    unittest.main()

