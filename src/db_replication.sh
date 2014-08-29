#!/bin/bash

# Script to replicate 2 databases in real time.
#=============================================================================
#Name           : 
#Author         : Praneeth Vallem (praneethkits@gmail.com),
#                 Nikhil(nikhilraog@gmail.com
#Date           : 08-28-2014
#version        : 1.0
#=============================================================================

lock_file='/var/log/db_replication.lock'
log_file='/var/log/db_replication_'`date +%Y%m%d_%H%M%S`.log

echo $log_file

# Check if program is running.
# ============================================================================
if [ -f ${lock_file} ]; then
    echo "ERROR: A process is running, wait until process is completed." >> $log_file
    exit 2
fi

# Create a lock file so that other process do not start
#=============================================================================
touch $lock_file

# Open the file where time stap is being stored
#=============================================================================
. ./replication.conf

# Function to clean up the temp files and log files
#=============================================================================
CLEAN_UP(){
    # remove all the files that were created in the process
    rm -rf ${lock_file}
}

LOG(){
    # write the message to log file
    echo $1 >> $log_file
}

# Check for the given parameters
#=============================================================================
if [ $# -ne 1 ]; then
    echo "Wrong number of parameters are passed"
    echo "Usage: sh db_replication.sh <db_name>"
    LOG "ERROR: Wrong Number of parameters Passed"
    CLEAN_UP
    exit 2
fi

mkdir -p /tmp/replication/$1
temp_sql_log="/tmp/replication/$1/temp.log"

GET_DB_LOG(){
    if [ $1 == 'remote' ]; then
        log_dir=$remote_log_dir
        log_base=$remote_log_base
    elif [ $1 == 'local' ]; then
        log_dir=$local_log_dir
        log_base=$local_log_base
    else
        LOG "ERROR: Invalid parameter passed to GET_DB_LOGS function"
        CLEAN_UP
        exit 2
    fi

    cd ${log_dir}
    mysqlbinlog `ls ${log_base}.* | grep -v '*.index'` > ${temp_sql_log}

}

REMOTE_CONNECT(){
    ssh ${host_user}@${ip_address}
}

REMOTE_DISCONNECT(){
    exit;
}

SCP(){
    local_file=$1
    remote_file=$2
    put_or_get=$3

    if [ ${put_or_get} == 'put' ]; then
        scp ${local_file} ${host_user}@${ip_address}:${remote_file}
        ret=$?
        if [ $? != 0 ]; then
            LOG "ERROR: scp of $local_file to $remote_file failed."
            CLEAN_UP 
