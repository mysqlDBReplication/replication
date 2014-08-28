#!/usr/bin/env python
""" This script is used to detect if there are any changes in the file from
    this given time."""

# Global variables defined to return success or failure
SUCCESS = True
FAILURE = False

import os
import commands
import logging
import general_utils
LOCATION = os.path.dirname(os.path.abspath(__file__))
os.chdir(LOCATION)
commands.getstatusoutput("make clean")
commands.getstatusoutput("make")
import config_pb2
from google.protobuf.text_format import Merge

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
            time = int(out.split('=')[1])
            return SUCCESS, time

    def get_previous_changed_time(self):
        """This function is used to get the timestamp when last time, databases
        were replicated."""
        if not self.replication_details.HasField('timestamp'):
            self.merge_config_protobuf()
        return self.replication_details.timestamp

    def get_log_file(self):
        """This function is used to return the log file name."""
        if not self.replication_details.HasField('log_file'):
            self.merge_config_protobuf()
        return self.replication_details.log_file

    def get_previous_index_pos(self):
        """This function is used to return the index position until which
        databases are replicated."""
        if not self.replication_details.HasField('index_pos'):
            self.merge_config_protobuf()
        return self.replication_details.index_pos

    def get_index_file(self):
        """This function is used to get the index file."""
        if not self.replication_details.HasField('index_file'):
            self.merge_config_protobuf()
        return self.replication_details.index_file
        
    def merge_config_protobuf(self):
        """This function is used to merge the config details from the lookup
        file with replication_details variable.
        Args:
            self: Instance of the class.
        Returns:
            True on success else False.
        Raises:
            NA.
        """
        if not general_utils.merge_proto(self.lookup_file,
                                         self.replication_details, 'Text'):
            logging.error("Merging of proto file failed")
            return FAILURE

        return SUCCESS

    def check_changes(self):
        """This function is used to check the changes in the log file and
        index file.
        Args:
            self: Instance of the class.
        Returns:
            True on Succses else False.
            Yes if there are changes else No.
        Raises:
            NA.
        """
        if not self.merge_config_protobuf():
            logging.error("Parsing the given protobuf file failed.")
            return FAILURE, 'No'

        index_file = self.get_index_file()
        log_file = self.get_log_file()
        previous_timestamp = self.get_previous_changed_time()
        logging.info("previous timestamp is " + str(previous_timestamp))

        status, log_timestamp = self.get_last_changed_time(log_file)
        if not status:
            logging.error("Unable to get the time stamp of \"%s\"", log_file)
            return FAILURE, 'No'
        logging.info("log file timestamp is " + str(log_timestamp))

        status, index_timestamp = self.get_last_changed_time(index_file)
        if not status:
            logging.error("Unable to get the time stamp of \"%s\"", index_file)
            return FAILURE, 'No'
        logging.info("index file timestamp is " + str(index_timestamp))

        if log_timestamp > previous_timestamp or\
                index_timestamp > previous_timestamp:
            return SUCCESS, 'Yes'
        else:
            return SUCCESS, 'No'
