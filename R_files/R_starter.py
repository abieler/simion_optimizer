from MySQLdb import *
from ftplib import FTP


id_r = 2
number_of_cores = 8
#simion_dir = '"C:\\Program Files (x86)\\SIMION 8.0\\mystuff\\'
simion_dir = '"C:\\Program Files\\SIMION-8.1\\mystuff\\'

while True:
	ftp = FTP('130.92.145.79')
	ftp.login('R','optimizer')
	break
	
print 'connected to FTP server'
ftp.retrbinary('RETR calculate_R_2.py', open('calculate_R_2.py','wb').write)
ftp.retrbinary('RETR calculate_R_functions.py', open('calculate_R_functions.py', 'wb').write)
ftp.retrbinary('RETR calculate_target_function.py', open('calculate_target_function.py', 'wb').write)

execfile('calculate_R_2.py')
