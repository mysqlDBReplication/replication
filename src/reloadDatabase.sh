#script to download the sql binary log files and reload the database
#===================================================================
#Name : dbReload.sh
#created by : Praneeth Vallem (praneethkits@gmail.com)
#created date : 16th may 2013
#version : 1.0
#===================================================================

#opening the configuration file to get the address of the files
#=============================================================
. ./dbConfig.conf

#get the files from the internet
#===============================
wget $fullAddress

#getting the filenames
#=====================
fileName=`echo $fullAddress | cut -d ' ' -f1 | cut -d '.' -f1`

indexFile=${fileName}.index

#check if the index file exist
#=============================
if [ ! -f $indexFile ]; then
	echo the index file doesnot exits 
	exit 2
fi

#Checking if each and every file listed in the index file exist
#==============================================================
for line in `cat $indexFile`
do
	binFile=`basename $line`
	if [ ! -f $binFile ]; then
		echo $binFile given in the $indexFile does not exits
		exit 2
	fi
done

#ask the user to give the username and password for the database
#===============================================================
echo enter the username of database
read userName

echo enter the password of the database
read password

#test if the templogfile exits and remove if it exits
#====================================================
if [ -f tempLogFile ]; then
	rm tempLogFile
fi

#changing the binary log files to acii file
#==========================================
for line in `cat $indexFile`
do
	binFile=`basename $line`
	mysqlbinlog $binFile >> tempLogFile
done

#Loading the databack into the database
#======================================
mysql -u$userName -p$password < tempLogFile

returnVal=$?
if [ $returnVal -ne 0 ]; then
	echo there is some error in loading the database
	exit 2
fi

#Removing the temporary logfile
#==============================
rm tempLogFile

echo database loaded successfully
exit 0;

