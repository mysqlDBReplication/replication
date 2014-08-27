#!/usr/bin/env python
""" This script is used to detect if there are any changes in the file from
    this given time."""

# Global variables defined to return success or failure
SUCCESS = True
FAILURE = False

import os
import commands
import logging
LOCATION = os.path.dirname(os.path.abspath(__file__))
os.chdir(LOCATION)
commands.getstatusoutput("make clean")
commands.getstatusoutput("make")
import config_pb2


class detectChanges(object):
    """ This class is used to detect changes in a given file.
    Attributes:
        NA.
    """

    def __init__(self, lookup_file):
        """Initializes the variables required by the class.
        Args:
            lookup_file: File in which previous timestamp is written.
        """
        self.lookup_file = lookup_file
        self.replication_details = config_pb2.previousReplicationDetails()

    def get_last_changed_time(self, file_name):
        """This function is used to get the last changed time stamp of the
        file.
        Args:
            self: instance of the class.
            file_name: Name of the file for which last changed timestamp need
                       to be found.
        Returns:
            True on success else False.
            If success returns the time stamp.
        Raises:
            NA.
        """
        command = "".join(["stat -c --format=%Z ", file_name])
        status, out = commands.getstatusoutput(command)
        if status != 0:
            logging.error("Unable to find the timestamp of \"%s\" due to %s",
                          file_name, out)
            return FAILURE, 0
        else:
            logging.info("Timestamp of file \"%s\" returned is %s", file_name,
                         out)
            time = out.split('=')[1]
            return SUCCESS, time

    def get_previous_changed_time(self):
        """This function is used to get the timestamp when last 2 databases
        were replicated."""
        return self.replication_details.timestamp

    def get_previous_replication_details(self):
        """This Function is used to get the previous replication details and
        Merge them into self.replication_details variable."""
        pass
