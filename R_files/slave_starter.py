from MySQLdb import *
from ftplib import FTP

def get_settings():
    myID = None
    nCores = None
    IP = None
    USER = None
    PW = None
    
    with fid = open("slave.config", "r"):
        for line in fid:
            key,value = line.strip().split(":")
            if key == "ID":
                myID = int(value)
            elif key == "nCores":
                nCores = int(value)
            elif key == "FTP_IP":
                IP = value
            elif key == "FTP_0USER":
                USER = key
            elif key == "FTP_PW":
                PW = key

    if not all([myID, nCores, IP, USER, PW):
        print "Error: Did not find all necessary information in slave.config."
        print ""
        print "Provide the following keywords in slave.config:"
        print "ID"
        print "nCores"
        print "FTP_IP"
        print "FTP_USER"
        print "FTP_PW"
        print ""
        print "All entries must be in the form keyword:value, such as "
        print "ID:2"
        print "FTP_IP:130.92.145.79"
        print "."
        print "."        
        print "etc."
        print ""
        print "Exiting now..."
        sys.exit()
        
    return myID, nCores, IP, USER, PW

# set some global variables
# these variables are also visible in slave_main.py namespace
myID, nCores, FTP_IP, FTP_USER, FTP_PW = get_settings()

while True:
    ftp = FTP(FTP_IP)
    ftp.login(FTP_USER, FTP_PW)
    break

print 'connected to FTP server'
ftp.retrbinary('RETR slave_main.py', open('slave_main.py','wb').write)
ftp.retrbinary('RETR slave_funcs.py', open('slave_funcs.py', 'wb').write)
ftp.retrbinary('RETR calculate_target_function.py', open('calculate_target_function.py', 'wb').write)

execfile('slave_main.py')
