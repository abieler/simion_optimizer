from __future__ import division
import os, sys
import time
import pickle
from MySQLdb import *
from scipy import *
from ftplib import FTP


def get_simion_files(FTP_IP, FTP_USER, FTP_PW):
    refiner_list = []
    gemfile_exists = False
    ftp = FTP(FTP_IP)
    ftp.login(FTP_USER, FTP_PW)
    print 'connected to FTP server'

    for file in ftp.nlst():
        if not file[-3:] == '.py':
            print 'start copying of file ' + str(file)
            ftp.retrbinary('RETR '+file, open(file, 'wb').write)
    for file in ftp.nlst():
        if file[-1] == '#':
            refiner_list.append(file)
        elif file[-1] == 'm':
            gemfile_exists = True
            gemfile_name = file
        elif file[-1] == 'b':
            iob_filename = file
        
    print 'refiner_list = ' + str(refiner_list)
    return refiner_list, gemfile_exists, gemfile_name, iob_filename


def delete_old_files(new_gem):
    ending_list = ['.pa*','.fly2', '.rec','.ion', '.lua', '.PA*', '.gem' ]
    if int(new_gem) == 1:
        for ending in ending_list:
            os.system('del *' + ending)
        
    os.system('del *.tmp')
    os.system('del optimizer_*_data.txt')
    
def fastadjust_voltages(paname,electrodes,voltages, SIMION_PATH, SIMION_BIN):
    if paname != 'None':
        s = SIMION_BIN + " --nogui fastadj " + SIMION_PATH + paname + '" '
        for electrode_number, electrode_voltage in zip(electrodes, voltages):
            s = s + str(electrode_number) + "=" + str(electrode_voltage) + ","
        s = s[:-1]
        return s
    else:
        s = ''
        return s
    
def fastadjust_all_fixed_voltages(PA_filenames,fix_electrodes,fix_voltages,simion_dir):
    for k in range(3):
        try:
            s = fastadjust_voltages(eval('PA_filenames['+ str(k) +']'), eval('fix_electrodes[' + str(k) + ']'), eval('fix_voltages[' + str(k) + ']'),simion_dir)
            if len(eval('fix_electrodes[' + str(k) + ']')) > 0:
                os.system(s)
                #print s
        except:
            pass


def fastadjust_adj_voltages_and_fly_ions(x, iob_filename, i):

    s = "'fly --recording-output=optimizer_%i_data.txt --restore-potentials=0 --retain-trajectories=0" %i
    s = s + ' ' + str(iob_filename) + "'"
    fid = open('start_simion_session_%i.lua' %i, 'w')
    fid.write("file = io.open('finished_" + str(i) + ".txt', 'w') \n")
    fid.write("file:write('0')\n")
    fid.write("file:close()\n")
    for j in range(len(x)):
        fid.write('_G.V' + str(j+1) + '=' + str(x[j]) + '\n')
    fid.write('simion.command(' + s + ')')
    fid.write('\n')
    fid.write("file = io.open('finished_" + str(i) + ".txt', 'w') \n")
    fid.write("file:write('1')\n")
    fid.write("file:close()")
    fid.close()
        
def get_sql_settings():
    IP = None
    USER = None
    PW = None
    DB = None

    with fid = open("slave.config", "r"):
        for line in fid:
            key,value = line.strip().split(":")
            if key == "SQL_IP":
                IP = value
            elif key == "SQL_USER":
                USER = value
            elif key == "SQL_PW":
                PW = value
            elif key == "SQL_DB":
                DB = value
    if not all([IP, USER, PW, DB]):
        print "Error: Did not find all necessary information in slave.config."
        print ""
        print "Provide the following keywords in slave.config:"
        print "SQL_IP"
        print "SQL_USER"
        print "SQL_PW"
        print "SQL_DB"
        print ""
        print "All entries must be in the form 'keyword:value', such as "
        print "SQL_IP:130.92.145.79"
        print "SQL_USER:userName"
        print "."
        print "."        
        print "etc."
        print ""
        print "Exiting now..."
        sys.exit()
        
def get_simion_settings():
    PATH = None
    SIMION_BIN = None

    with fid = open("slave.config", "r"):
        for line in fid:
            key,value = line.strip().split(":")
            if key == "SIMION_PATH":
                PATH = value
            elif key == "SIMION_BIN":
                SIMION_VER = value

    if not all([PATH, SIMION_VER]):
        print "Error: Did not find all necessary information in slave.config."
        print ""
        print "Provide the following keywords in slave.config:"
        print "SIMION_PATH"
        print "SIMION_BIN"
        print "Exiting now..."
        sys.exit()

    return PATH, SIMION_BIN

def mysql_connect():
    host, user, pw, db = get_sql_settings()
    try:
        verb = connect(host=host, user=user, db=db, passwd=pw)
        return verb
    except Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        time.sleep(2)
        sys.exit()
        
def write_zielf(myID, zielf): #zielf ist eine list mit den zielfunktionen in der richtigen reihenfolge
    
    for i in range(25):
        try:
            id_r_str = str(myID) 
            datenbank = mysql_connect()
            cursor = datenbank.cursor (cursors.DictCursor)
            
            cursor.execute ("SELECT job_id FROM jobs WHERE id_R = '"+id_r_str+"' AND status = '1' ORDER BY part_volt_id")
            result_set = cursor.fetchall()
            print len(zielf)
            print cursor.rowcount
            i=0
            for key in result_set:
                job_id_tmp = key['job_id']
                cursor.execute ("UPDATE jobs SET zielfunktion = '" + str(zielf[i]) + "', status = '2' WHERE status = '1' AND job_id = '" + str(job_id_tmp) + "' AND id_R = '" + id_r_str + "' LIMIT 1")
                i+=1
            datenbank.commit ()
            datenbank.close ()
            return True
        except:
            time.sleep(1)
    

def algo_param(myID, nCores):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    db = mysql_connect()
    
    while True:
    
        try:
            cursor = db.cursor(cursors.DictCursor)
            print 'getting jobs'
            cursor.execute("UPDATE jobs SET status = '1', id_R = %s WHERE status = '0' LIMIT %i" % (str(myID), nCores) )
            print 'getting job id'
            cursor.execute("SELECT job_id from jobs WHERE status = '1' AND id_R = %s" % (str(myID)) )
            db_data = cursor.fetchall()

            X = []
            for d in db_data:
                job_id = int(d["job_id"])
                cursor.execute("SELECT voltage from voltages WHERE job_id = %s ORDER BY volt_id" % (str(job_id)))
                voltages = cursor.fetchall()
                x = []
                for volt in voltages:
                    x.append(float(volt["voltage"]))

                print 'job_id  = %i' % job_id
                print 'voltages= ' + str(x)

                X.append(x)

            cursor.execute("SELECT volt_it_id from jobs WHERE job_id = %s" % (str(job_id)))
            db_data = cursor.fetchall()
            
            volt_iteration = int(db_data[0]["volt_it_id"])
            
            return X, volt_iteration
        except:
            print 'did not find any free jobs'
            time.sleep(0.5)
