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

# Check for the given parameters
#=============================================================================
if [ $# -ne 1 ]; then
    echo "Wrong number of parameters are passed"
    echo "Usage: sh db_replication.sh <db_name>"
    echo "ERROR: Wrong number of parameter passed" >> $log_file
    exit 2
fi

echo $log_file
mkdir -p /tmp/replication/$1
temp_sql_log="/tmp/replication/$1/temp.log"
temp1_sql_log="/tmp/replication/$1/temp1.log"
sql_log="/tmp/replication/$1/db.sql"
db_name=$1

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
    rm -rf ${lock_file} ${temp1_sql_log}
}

LOG(){
    # write the message to log file
    echo $1 >> $log_file
}

GET_DB_LOG(){
    if [ $1 = 'remote' ]; then
        log_dir=$remote_log_dir
        log_base=$remote_log_base
    elif [ $1 = 'local' ]; then
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
    ssh ${host_user}@${ip_address} -o ConnectTimeout=${connection_time_out}
    ret=$?
    if [ $ret -ne 0 ]; then
	LOG "ERROR: Unable to connect to ${ip_address}"
	CLEAN_UP
	exit 2
    fi
}

REMOTE_DISCONNECT(){
    exit;
}

SCP(){
    local_file=$1
    remote_file=$2
    put_or_get=$3

    if [ ${put_or_get} = 'put' ]; then
        scp -o ConnectTimeout=${connection_time_out} ${local_file} ${host_user}@${ip_address}:${remote_file}
        ret=$?
        if [ $? != 0 ]; then
            LOG "ERROR: scp of $local_file to $remote_file failed."
            CLEAN_UP
            exit 2
	fi
    elif [ ${put_or_get} = 'get' ]; then
        scp -o ConnectTimeout=${connection_time_out} ${host_user}@${ip_address}:${remote_file} ${local_file}
        ret=$?
        if [ $? != 0 ]; then
            LOG "ERROR: scp of $remote_file to $local_file failed."
            CLEAN_UP
            exit 2
        fi
    fi 
}

GET_DIFF(){
    sed -n '/use ${db_name}\/\*\/\;/,/use/'p ${temp_sql_log} | sed '/use/d' > ${temp1_sql_log}
    mv ${temp1_sql_log} ${temp_sql_log}

    diff ${sql_log} ${temp_sql_log} | sed -n '/^>/'p | cut -c2-500000 > ${temp1_sql_log}
}

EXECUTE_DIFF(){
    if [ $1 = 'remote' ]; then
	user=${remote_db_user}
	pass=${remote_db_pass}
    elif [ $1 = 'local' ]; then
        user=${local_db_user}
        pass=${local_db_pass}
    fi

    sed -i 11 "SET sql_log_bin = 0;" ${temp1_sql_log}
    mysql -u${user} -p${pass} ${db_name} < ${temp1_sql_log}
    ret=$?
    if [ $ret != 0 ]; then
	echo "Diff execution failed"
	LOG "ERROR: Diff execution in $1 failed"
	CLEAN_UP
	exit 2
    fi

    mv ${temp_sql_log} ${sql_log}
}

GET_DB_LOG 'local'
SCP ${temp_sql_log} ${temp_sql_log} 'put'
REMOTE_CONNECT
GET_DIFF
EXECUTE_DIFF 'remote'
GET_DB_LOG 'remote'
CLEAN_UP
REMOTE_DISCONNECT
SCP ${temp_sql_log} ${temp_sql_log} 'get'
GET_DIFF
EXECUTE_DIFF 'local'

CLEAN_UP
exit 0
