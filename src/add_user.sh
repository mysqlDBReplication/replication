# This script is used add user and the upload folder and set its permissions
#!/usr/local/bin/expect -f




# Check for the number of parameters given
# ========================================
if [ $# != 2 ]; then
    echo "Wrong number of parameters passed"
    echo "Usage: sh add_user.sh <userid> <password> <user name>"
    exit 2;
fi

# Multiple group names can be given here saperate them with a comma.
#==================================================================
GROUP_NAME='clients'


# Create a new user with the given credentials
# ============================================
sudo su -c "useradd $1 -s /bin/bash -m -G ${GROUP_NAME}"

# The following commands changes the password and needs expect tool(apt-get install expect)
# =========================================================================================
spawn ${env} (SHELL)
send -- "passwd $1\r"
expect "password:"
send "$2\r"
expect "password:"
send "$2\r"
send "\r"
expect eof
