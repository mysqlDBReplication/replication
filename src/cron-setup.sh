# This script is used to setup the cron job
# =========================================

# Check for the number of parameters passed.
# ==========================================
if [ $# -ne 2 ]; then
    echo "Wrong number of parameters passed."
    echo "Usage sh cron-setup.sh <command(encode in single quotes)> <interval in min>"
    exit 2
fi

# Get the current configs into the file
# =====================================
crontab -l > temp.cron
ret=$?
if [ $ret -ne 0 ]; then
    echo "cron job is not setup"
    exit 2
fi
sed -i "s@.*$1.*@@" temp.cron
sed -i /^$/d temp.cron

# Add the given script to the cron 
# ================================
echo "*/$2 * * * * $1" >> temp.cron
crontab < temp.cron
ret=$?
if [ $ret -ne 0 ]; then
    echo "unable to setup the cron job."
    exit 2
fi

cat temp.cron
rm temp.cron
exit 0
