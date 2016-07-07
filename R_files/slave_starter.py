from MySQLdb import *
from ftplib import FTP
import sys

def get_settings():
    myID = None
    nCores = None
    IP = None
    USER = None
    PW = None

    with open("slave.config", "r") as fid:
        for line in fid:
            try:
                key,value = line.strip().split("::")
                if key == "ID":
                    myID = int(value)
                elif key == "nCores":
                    nCores = int(value)
                elif key == "FTP_IP":
                    IP = value
                elif key == "FTP_USER":
                    USER = key
                elif key == "FTP_PW":
                    PW = key
            except Exception, e:
                pass

    if not all([myID, nCores, IP, USER, PW]):
        print "Error: Did not find all necessary information in slave.config."
        print ""
        print "Provide the following keywords in slave.config:"
        print "ID"
        print "nCores"
        print "FTP_IP"
        print "FTP_USER"
        print "FTP_PW"
        print ""
        print "All entries must be in the form 'keyword:value', such as "
        print "ID:2"
        print "FTP_IP:130.92.145.79"
        print "."
        print "."
        print "etc."
        print ""
        print "Found following settings in the slave.config file:"
        print "myID    :\t", myID
        print "nCores  :\t", nCores
        print "IP      :\t", IP
        print "FTP_USER:\t", USER
        print "FTP_PW  :\t", PW
        print
        print "Exiting now..."
        sys.exit()

    return myID, nCores, IP, USER, PW

# set some global variables
# these variables are also visible in slave_main.py namespace
myID, nCores, FTP_IP, FTP_USER, FTP_PW = get_settings()
IS_DEBUG = True

if not IS_DEBUG:
    print " - connecting to FTP server"
    while True:
        ftp = FTP(FTP_IP)
        ftp.login(FTP_USER, FTP_PW)
        break
else:
    print " - DEBUG mode: did not actually connect to FTP server"

if not IS_DEBUG:
    print ' - FTP server connection OK'
    ftp.retrbinary('RETR slave_main.py', open('slave_main.py','wb').write)
    ftp.retrbinary('RETR slave_funcs.py', open('slave_funcs.py', 'wb').write)
    ftp.retrbinary('RETR calculate_target_function.py', open('calculate_target_function.py', 'wb').write)
else:
    print " - DEBUG mode: did not copy .py files from master slave"

execfile('slave_main.py')
