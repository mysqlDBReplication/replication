# This script is used add user and the upload folder and set its permissions
set -x

# Check for the number of parameters given
# ========================================
if [ $# != 3 ]; then
    echo "Wrong number of parameters passed"
    echo "Usage: sh add_user.sh <userid> <password> <Group>"
    exit 2;
fi

# Multiple group names can be given here saperate them with a comma.
#==================================================================
GROUP_NAME=$3
USER_NAME=$1
PASSWORD=$2

# Check if the given user exists
# ==============================
grep -i "^${USER_NAME}" /etc/passwd >> /dev/null 
ret=$?
if [ ${ret} -eq 0 ]; then
    echo "Given User exists"
    exit 2;
fi

# Check if the given group exits else create it.
# ==============================================
grep -i "^${GROUP_NAME}" /etc/group >> /dev/null
ret=$? 
if [ $ret -ne 0 ]; then
    sudo groupadd${GROUP_NAME}
fi

# Create a new user with the given credentials
# ============================================
pass=$(perl -e 'print crypt($ARGV[0], "password")' $2)
sudo adduser $1 -p ${pass} -s /bin/bash -m -G ${GROUP_NAME}
ret=$?
if [ $ret -ne 0 ]; then
    echo "user creation failed."
    exit 2
fi

# Create a upload directory and change the permissions for the same
# =================================================================
sudo mkdir -p /home/$1/db_upload
ret=$?
if [ $ret -ne 0 ]; then
    echo "user creation failed."
    exit 2
fi
sudo chmod 600 /home/$1/db_upload
ret=$?
if [ $ret -ne 0 ]; then
    echo "Failed to create a db_upload folder."
    exit 2
fi
sudo chown $1 /home/$1/db_upload
ret=$?
if [ $ret -ne 0 ]; then
    echo "Failed to change the owner of db_upload folder."
    exit 2
fi
sudo chgrp $1 /home/$1/db_upload
ret=$?
if [ $ret -ne 0 ]; then
    echo "Failed to chnage the group of db_upload folder."
    exit 2
fi

echo "user created."
exit 0
