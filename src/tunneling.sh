# This script is used to create a tunnel to the cloud vm
# ======================================================
# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

# Check for the number of parameters passed.
# ==========================================
if [ $# -ne 3 ]; then
    echo "Wrong number of parameters passed."
    echo "Usage: sh tunneling.sh <ip address> <port number> <userid>"
    exit 2
fi

ip_address=$1
port=$2
user=$3

ssh -f -R ${port}:localhost:3306 ${user}@${ip_address} sleep 365d

echo "ip_address=$ip_address" > $SCRIPTPATH/.tunneling.conf
echo "port=$port" >> $SCRIPTPATH/.tunneling.conf
echo "dir=$SCRIPTPATH" >> $SCRIPTPATH/.tunneling.conf
echo "user=$user" >> $SCRIPTPATH/.tunneling.conf 
