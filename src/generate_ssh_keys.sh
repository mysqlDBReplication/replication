# This script is used to generate the ssh keys for the given user
# ===============================================================


# Check for the given number of parameters
# ========================================
if [ $# -ne 2 ]; then
    echo "Wrong number of parameters are passed."
    echo "Usage sh generate_ssh_keys.sh <file_name> <userid or emailid>"
    exit 2
fi

ssh-keygen -t rsa -N "" -f "$1" -C "$2"
ret=$?
if [ $ret -ne 0 ]; then
    echo "ssh key generation failed."
    exit 2
fi

eval "$(ssh-agent -s)"
ssh-add $1
ret=$?
if [ $ret -ne 0 ]; then
    echo "unable to add private key to authentication agent"
    exit 2
fi

