#!/usr/bin/env python
""" This script holds the various general utilities required."""

import commands
import logging
import time
from google.protobuf.text_format import Merge
from google.protobuf import descriptor

SUCCESS = True
FAILURE = False


def execute_command(command):
    """ This function is used to execute the given command.
    Args:
        command: Command that needs to be executed.
    Returns:
        True when command is executed else False.
        output of the command.
    Raises
        NA.
    """
    logging.info("Executing command: %s", command)
    out = commands.getstatusoutput(command)
    if out[0] != 0:
        logging.error(command)
        logging.error("Unable to execute above command due to::%s", out[1])
        return FAILURE, 'NA'
    else:
        return SUCCESS, out[1]


def read_file_contents(file_name=None):
    """This function is used to read the file contents and return contents
    in a string format.
    Args:
        file_name: file which need to be read.
    Returns:
        SUCCESS when successfully read else FAILURE
        file_content: Complete content of file.
    Raises:
        NA.
    """
    if file_name is None:
        return FAILURE, 'NA'
    try:
        file_descriptor = open(file_name, "rb")
    except IOError:
        logging.error("Unable to open given protobuf file")
        return FAILURE, 'NA'
    file_content = file_descriptor.read()
    file_descriptor.close()
    return SUCCESS, file_content


def wait(time_sec=None):
    """This function is used to wait for given amount of time.
    Args:
        time_sec: Time in seconds.
    Returns:
        True on completion.
    Raises:
        NA.
    """
    if time_sec is None:
        return True
    logging.info("".join(["waiting for ", str(time_sec), " seconds"]))
    time.sleep(time_sec)
    return True


def write(file_name=None, content=None, flags=None):
    """This function is used to write the given contents to given filename.
    Args:
        file_name: file to which content need to be written.
        content: content that need to be written
        flags: flags used to open file.
    Returns:
        SUCCESS when successfully read else FAILURE
    Raises:
        NA.
    """
    if file_name is None or content is None:
        return FAILURE
    if flags is None:
        flags = "a"
    try:
        file_descriptor = open(file_name, flags)
    except IOError:
        logging.error("Unable to open given file")
        return FAILURE
    file_descriptor.write(str(content))
    file_descriptor.close()
    return SUCCESS
