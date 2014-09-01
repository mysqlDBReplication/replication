set -x
# This script is used to check the tunnel peridoically and if not present restart the tunnel
# ==========================================================================================
dir=`dirname $0`

# open the configuration script.
# =============================
. $dir/.tunneling.conf

process_count=`ps -ef | grep "ssh -f -R $port:localhost:3306 ${user}@${ip_address}" | grep -v 'grep' | wc -l`
if [ $process_count -le 0 ]; then
	sh ${dir}/tunneling.sh ${ip_address} ${user} ${port}
fi
