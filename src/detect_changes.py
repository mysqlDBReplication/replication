#!/usr/bin/env python
""" This script is used to detect if there are any changes in the file from
    this given time."""

# Global variables defined to return success or failure
SUCCESS = True
FAILURE = False

import os
import commands
import logging


class detectChanges(object):
    """ This class is used to detect changes in a given file.
    Attributes:
        NA.
    """

    def __init__(self):
        """Initializes the variables required by the class."""
        logging.info("In constructor of detectChanges class.")

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
