# This script is used to detect the chnages in the database and upload the logfiles to cloud.
# ===========================================================================================
set -x


# Check for the number of parameters given.
# =========================================
if [ $# -ne 0 ]; then
    echo "wrong number of parameters passed."
    echo "Usage sh db_upload.sh"
    exit 2
fi

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

mkdir -p /var/log/replication
log_file=/var/log/replication/db_upload_`date +%Y%m%d_%H%M%S`
lock_file=/var/log/replication/db_upload.lock

if [ -f $lock_file ]; then
    echo "A process is running, please wait until the process is completed." >> $log_file
    echo A process is running, please wait until the process is completed.
    exit 2
fi
touch $lock_file

# Open the timestamp file
# =======================
. $SCRIPTPATH/.dbupload.conf || rm -rf $lock_file >> $log_file

# get the mysql log directory
# ===========================
if [ -f /etc/my.cnf ]; then
    filename=/etc/my.cnf
elif [ -f /etc/mysql/my.cnf ]; then
    filename=/etc/mysql/my.cnf
fi

logline=`grep '^log_bin' $filename | tr -d " " | tr -d "\t" | cut -d"=" -f2`
if [ -z $logline ]; then
    echo "Logging is not enabled in the mysql server."
    echo "Logging is not enabled in the mysql server." >> $log_file
    rm -rf $lock_file
    exit 2
fi
logdir=`dirname $logline`
dbfile=`basename $logline | rev | cut -d"." -f2-100 | rev`

# detect the changes in file list
# ===============================
for file in `ls -tr $logdir/${dbfile}*`
do
    changedtime=`stat -c --format=%Z $file | cut -d"=" -f2`
    if [ $changedtime -gt $timestamp ]; then
        file_list="$file_list $file"
    fi
done

# Upload the file list to server
# =============================
echo \"$file_list\"
if [ ! -z "$file_list" ]; then
    scp ${file_list} $username@$ip_address:~/db_upload/
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "unable to upload the files"
        echo "unable to upload the files." >> $log_file
        rm -rf $lock_file
        exit 2
    fi
    echo "username=$username" > $SCRIPTPATH/.dbupload.conf
    echo "ip_address=${ip_address}" >> $SCRIPTPATH/.dbupload.conf
    echo "timestamp=$changedtime" >> $SCRIPTPATH/.dbupload.conf
fi

# Remove the lock file and exit
# =============================
rm -rf $lock_file
echo "successfully uploaded."
echo "successfully uploaded." >> $log_file
exit 0


# 
