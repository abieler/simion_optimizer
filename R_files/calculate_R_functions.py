from __future__ import division
import os, sys
import time
import pickle
from MySQLdb import *
from scipy import *
from ftplib import FTP

'''
def calculate_target_function(number_of_particles):
	target_function = []
	worst_target_function_value = 0
	
	
	for index in range(number_of_particles):
		TF = worst_target_function_value
		nr,tof,m,x,y,z,az,el,vx,vy,vz,pot,ke = [], [], [], [], [], [], [], [], [], [], [], [], []
		nr_D,tof_D,m_D,x_D,y_D,z_D,az_D,el_D,vx_D,vy_D,vz_D,pot_D,ke_D = [], [], [], [], [], [], [], [], [], [], [], [], []

		NR,TOF,M,X,Y,Z,AZ,EL,VX,VY,VZ,POT,KE = 0,0,0,0,0,0,0,0,0,0,0,0,0
		try:
			file = open('optimizer_' + str(index) + '_data.txt','r')
			for line in file:
				try:
					NR,TOF,M,X,Y,Z,AZ,EL,VX,VY,VZ,POT,KE = line.split(',')
					nr.append(int(NR))
					tof.append(float(TOF))
					m.append(float(M))
					x.append(float(X))
					y.append(float(Y))
					z.append(float(Z))
					az.append(float(AZ))
					el.append(float(EL))
					vx.append(float(VX))
					vy.append(float(VY))
					vz.append(float(VZ))
					pot.append(float(POT))
					ke.append(float(KE))
					
				except:
					pass
			
			for NR,TOF,M,X,Y,Z,AZ,EL,VX,VY,VZ,POT,KE in zip(nr,tof,m,x,y,z,az,el,vx,vy,vz,pot,ke):
				try:

					if(19.99 < X < 20.01):
						nr_D.append(NR)
						tof_D.append(TOF)
						m_D.append(M)
						x_D.append(X)
						y_D.append(Y)
						z_D.append(Z)
						az_D.append(AZ)
						el_D.append(EL)
						vx_D.append(VX)
						vy_D.append(VY)
						vz_D.append(VZ)
						ke_D.append(KE)


				except:
					pass
			try:
				########################################################
				####### CALCULATE THE TARGET FUNCTION HERE #############
				########################################################
				
				if len(x_D) > 1:
					transmission = len(x_D)/len(x) * 100
					resolution = mean(tof_D)/(2*std(tof_D)*2)
					
					if transmission < 10:
						TF = -transmission
					elif transmission >= 10:
						TF = -resolution
				else:
					TF = 1

				
				try:
					f = open('tf_control.txt','r')
					tf_control = pickle.load(f)
					f.close()
					if TF < tf_control:
						f = open('tf_control.txt','w')
						pickle.dump(TF,f)
						f.close()
						
						f = open('tf_control_file.txt','a')
						f.write('target funct = ' + str(TF) + '\n')
						f.write('transmission = ' + str(transmission) + '\n')
						f.write('resolution   = ' + str(resolution) + '\n')
						f.write('********************************************* \n')
						f.close()
				except:
					f = open('tf_control.txt','w')
					pickle.dump(TF,f)
					f.close()
					
					f = open('tf_control_file.txt','a')
					f.write('target funct = ' + str(TF) + '\n')
					f.write('transmission = ' + str(transmission) + '\n')
					f.write('resolution   = ' + str(resolution) + '\n')
					f.write('********************************************* \n')
					f.close()
				
			

				target_function.append(TF)
				
				########################################################
				########################################################
				########################################################
			except:
				print 'could not calculate Target function!'
				time.sleep(2)
				target_function.append(worst_target_function_value)

		except:
			target_function.append(worst_target_function_value)
			print 'could not open simion data file'
			
			
			
	return target_function
'''

def get_simion_files_2():	
	
	
	refiner_list = []
	gemfile_exists = False
	#ftp = FTP('130.92.144.62')
	#ftp.login('r','optimizer')
	ftp = FTP('130.92.145.79')
	ftp.login('R','optimizer')
	print 'connected to FTP server'

	for file in ftp.nlst():
		if not file[-3:] == '.py':
			print 'start copying of file ' + str(file)
			ftp.retrbinary('RETR '+file, open(file, 'wb').write)
	for file in ftp.nlst():
		if file[-1] == '#':
			refiner_list.append(file)
		elif file[-1] == 'm': #if there is a gemfile
			gemfile_exists = True
			gemfile_name = file
		elif file[-1] == 'b':
			iob_filename = file
		
	print 'refiner_list = ' + str(refiner_list)
	return refiner_list,gemfile_exists,gemfile_name,iob_filename
	
	

def get_simion_files(iob_filename,PA_filenames):
	refiner_list = []
	gemfile_exists = False
	gemfile_name = None
	#ftp = FTP('130.92.144.62')
	#ftp.login('r','optimizer')
	ftp = FTP('130.92.145.79')
	ftp.login('R','optimizer')
	print 'connected to FTP server'

	for file in ftp.nlst():
		if not file[-3:] == '.py':
			print 'start copying of file ' + str(file)
			ftp.retrbinary('RETR '+file, open(file, 'wb').write)
	for file in ftp.nlst():
		if file[-1] == '#':
			refiner_list.append(file)
		elif file[-1] == 'm': #if there is a gemfile
			gemfile_exists = True
			
		
	print 'refiner_list = ' + str(refiner_list)
	return refiner_list,gemfile_exists
			
		
def delete_old_files(new_gem):#,first_particle):
	if int(new_gem) == 1:# and first_particle == True: 
		ending_list = ['.pa*','.fly2', '.rec','.ion', '.lua', '.PA*', '.gem' ]
		
		for ending in ending_list:
			os.system('del *' + ending)
		
	os.system('del *.tmp')
	os.system('del optimizer_*_data.txt')
	
def fastadjust_voltages(paname,electrodes,voltages,simion_dir):
	if paname != 'None':
		s = "simion-8.0.6-TEST5-20100415.exe --nogui fastadj " + simion_dir + paname + '" '
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
'''			
def fastadjust_adj_voltages_and_fly_ions_2(X,iob_filename):
	for i in range(len(X)):
		s = '"fly --recording-output=optimizer_' + str(i) + '_data.txt --restore-potentials=0 --retain-trajectories=0'
		for j in range(len(X[0])):
			s = s + ' --adjustable _G.V' + str(j+1) + '=' + str(X[i][j])
		s = s + ' ' + str(iob_filename) + '"'
		#print s
		fodi = open('simion_commands.log','a')
		fodi.write(s + '\n')
		fodi.close()
		fid = open('start_simion_session_' + str(i) + '.lua', 'w')
		fid.write("file = io.open('finished_" + str(i) + ".txt', 'w') \n")
		fid.write("file:write('0')\n")
		fid.write("file:close()\n")
		fid.write('simion.command(' + s + ')')
		fid.write('\n')
		fid.write("file = io.open('finished_" + str(i) + ".txt', 'w') \n")
		fid.write("file:write('1')\n")
		fid.write("file:close()")
		fid.close()
'''	
def fastadjust_adj_voltages_and_fly_ions_2(x,iob_filename,i):
        
        
	s = "'fly --recording-output=optimizer_%i_data.txt --restore-potentials=0 --retain-trajectories=0" %i
	s = s + ' '+str(iob_filename) + "'"
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
		
		
def mysql_connect():
	host_var = '130.92.145.79'
	user_var = 'root'
	pw_var = 'optimizer'
	#user_var = 'andre'
	#pw_var = ''
	db_var = 'simion_optimizer_db'
	
	try:
		verb = connect(host=host_var,user=user_var,db=db_var,passwd=pw_var)
		return verb
	except Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		time.sleep(4)
		sys.exit()
		
def write_zielf(id_r,zielf): #zielf ist eine list mit den zielfunktionen in der richtigen reihenfolge
	
	for i in range(25):
		try:
			id_r_str = str(id_r) 
			datenbank = mysql_connect()
			cursor = datenbank.cursor (cursors.DictCursor)
			
			cursor.execute ("SELECT job_id FROM jobs WHERE id_R = '"+id_r_str+"' AND status = '1' ORDER BY part_volt_id")
			result_set = cursor.fetchall()
			print len(zielf)
			print cursor.rowcount
			i=0
			for key in result_set:
				job_id_tmp = key['job_id']
				cursor.execute ("UPDATE jobs SET zielfunktion = '"+str(zielf[i])+"', status = '2' WHERE status = '1' AND job_id = '"+str(job_id_tmp)+"' AND id_R = '"+id_r_str+"' LIMIT 1")
				i+=1
			datenbank.commit ()
			datenbank.close ()
			return True
		except:
			time.sleep(2)
	

def get_algo_param_3(id_r,number_of_cores):
	timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
	db = mysql_connect()
	
	while True:
	
		try:
			cursor = db.cursor(cursors.DictCursor)
			print 'getting jobs'
			cursor.execute("UPDATE jobs SET status = '1', id_R = %s WHERE status = '0' LIMIT %i" %(str(id_r),number_of_cores) )
			print 'getting job id'
			cursor.execute("SELECT job_id from jobs WHERE status = '1' AND id_R = %s" % (str(id_r)) )
			db_data = cursor.fetchall()
			
			
			X = []
			for d in db_data:
				job_id = int(d["job_id"])
				cursor.execute("SELECT voltage from voltages WHERE job_id = %s ORDER BY volt_id" % (str(job_id)))
				voltages = cursor.fetchall()
				x = []
				for volt in voltages:
					x.append(float(volt["voltage"]))
					
				print 'job_id  = %i' %job_id
				print 'voltages= ' + str(x)
				
				X.append(x)
				
				
			cursor.execute("SELECT volt_it_id from jobs WHERE job_id = %s" % (str(job_id)))
			db_data = cursor.fetchall()
			
			volt_iteration = int(db_data[0]["volt_it_id"])
			
			return X, volt_iteration
		except:
			print 'did not find any free jobs'
			time.sleep(0.5)

	
	
	
def get_algo_param2(id_r,number_of_cores):
	new_gem_flag = False
	
	timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
	id_r_str = str(id_r) #damits in den queries gleich geht
	datenbank = mysql_connect()
	cursor = datenbank.cursor (cursors.DictCursor)
	cursor.execute ("SELECT job_id FROM jobs WHERE status = '1' AND id_R = '"+id_r_str+"'")
	#cursor.execute ("SELECT job_id FROM jobs WHERE status = '0'")
	
	anz_rows = cursor.rowcount
	limit_rows = number_of_cores - anz_rows
	if anz_rows < number_of_cores: #wenn er schon acht jobs hat, keinen mehr holen
		cursor.execute("SELECT * FROM status_r WHERE R_id = '"+id_r_str+"'")
		result_set = cursor.fetchall()
		geom_it_id_aktuell_stat = -1
		geom_part_id_aktuell_stat = -1
		if(cursor.rowcount > 0):
			geom_it_id_aktuell_stat = result_set[0]['geom_it_id']
			geom_part_id_aktuell_stat = result_set[0]['geom_part_id']
		else:
			cursor.execute("INSERT INTO status_r (R_id,datetime,status,geom_it_id,geom_part_id) VALUES ('"+id_r_str+"','"+timestamp+"','0','-1','-1')")
		limit_str = str(limit_rows)
		cursor.execute("SELECT status FROM status_of_gem_particle WHERE geom_it_id = '"+str(geom_it_id_aktuell_stat)+"' AND geom_part_id = '"+str(geom_part_id_aktuell_stat)+"'")
		result_status_gem_part = cursor.fetchall()
		continue_search = False
		if(cursor.rowcount > 0):
			if(result_status_gem_part[0]['status'] == 0 ):
				continue_search = True
		
		while(continue_search):
			cursor.execute("SELECT status FROM status_of_gem_particle WHERE geom_it_id = '"+str(geom_it_id_aktuell_stat)+"' AND geom_part_id = '"+str(geom_part_id_aktuell_stat)+"'");
			result_status_gem_part = cursor.fetchall()
			if(cursor.rowcount > 0 and geom_it_id_aktuell_stat != '-1'):
				if(result_status_gem_part[0]['status'] == 1 ):#von HS gesetzt worden
					continue_search = False;
			
			print 'looking for new jobs'
			time_elapsed = 0
			t00 = time.time()
			while(time_elapsed < 20):
				cursor.execute("UPDATE jobs SET status = '3', id_R = '"+id_r_str+"', datetime = '"+str(timestamp)+"' WHERE status = '0' AND geom_it_id = '"+str(geom_it_id_aktuell_stat)+"' AND geom_part_id = '"+str(geom_part_id_aktuell_stat)+"' LIMIT "+limit_str)
				cursor.execute ("SELECT * FROM jobs WHERE status = '3' AND id_R = '"+id_r_str+"' ORDER BY part_volt_id")
				anz_rows = cursor.rowcount
				if(anz_rows > 0):
					print 'new jobs found'
					continue_search = False
					break
				if(geom_it_id_aktuell_stat == -1):
					break
				t11 = time.time()
				time_elapsed = t11 - t00
				time.sleep(0.05)

		#cursor.execute("UPDATE jobs SET status = '3', id_R = '"+id_r_str+"', datetime = '"+str(timestamp)+"' WHERE status = '0' AND geom_it_id = '"+str(geom_it_id_aktuell_stat)+"' AND geom_part_id = '"+str(geom_part_id_aktuell_stat)+"' LIMIT "+limit_str)
		#cursor.execute ("SELECT * FROM jobs WHERE status = '3' AND id_R = '"+id_r_str+"' ORDER BY part_volt_id")
		#anz_rows = cursor.rowcount
		if(anz_rows == 0):
			new_gem_flag = True
			cursor.execute("SELECT COUNT(job_id) AS anz_jobs, geom_it_id, geom_part_id FROM jobs WHERE status = '0' GROUP BY geom_it_id,geom_part_id ORDER BY anz_jobs DESC LIMIT 0,1")
			result_set = cursor.fetchall()
			geom_it_id_aktuell_stat = result_set[0]['geom_it_id']
			geom_part_id_aktuell_stat = result_set[0]['geom_part_id']
			cursor.execute("UPDATE status_r SET datetime = '"+str(timestamp)+"', geom_it_id = '"+str(geom_it_id_aktuell_stat)+"', geom_part_id = '"+str(geom_part_id_aktuell_stat)+"' WHERE R_id = '"+id_r_str+"'")
		
			cursor.execute("UPDATE jobs SET status = '3', id_R = '"+id_r_str+"', datetime = '"+str(timestamp)+"' WHERE status = '0' AND geom_it_id = '"+str(geom_it_id_aktuell_stat)+"' AND geom_part_id = '"+str(geom_part_id_aktuell_stat)+"' LIMIT "+limit_str)
			cursor.execute("SELECT * FROM jobs WHERE status = '3' AND id_R = '"+id_r_str+"' ORDER BY part_volt_id")
			anz_rows = cursor.rowcount
		
		result_set = cursor.fetchall()
		cursor.execute ("UPDATE jobs SET status = '1' WHERE status = '3' AND id_R = '"+id_r_str+"'")
		
		
		
		voltages_rueckgabe = []
		
		for key in result_set:
			particle_id = key['part_volt_id']
			iteration_id = key['volt_it_id']
			cursor.execute ("SELECT voltage FROM voltages WHERE geom_iteration_id = '"+str(geom_it_id_aktuell_stat)+"' AND geom_particle_id = '"+str(geom_part_id_aktuell_stat)+"' AND voltage_iteration_id = '"+str(iteration_id)+"' AND voltage_particle_id = '"+str(particle_id)+"' ORDER BY volt_id");
			voltages_set_tmp = cursor.fetchall()
			anz_rows_volt = cursor.rowcount
			voltages_rueckgabe_tmp = zeros([anz_rows_volt])
			i=0
			voltages_rueckgabe_tmp = []
			for key_volt in voltages_set_tmp:
				voltages_rueckgabe_tmp.append(key_volt['voltage'])
				i = i + 1
			
			voltages_rueckgabe.append(voltages_rueckgabe_tmp)
		
		#status fuer das gem Teilchen auf unfertig setzen
		#cursor.execute("INSERT INTO status_of_gem_particle (geom_it_id,geom_part_id,status) VALUES ('"+str(geom_it_id_aktuell_stat)+"','"+str(geom_part_id_aktuell_stat)+"','0') ON DUPLICATE KEY UPDATE status = '0'")
		cursor.execute("INSERT IGNORE INTO status_of_gem_particle (geom_it_id,geom_part_id,status) VALUES ('"+str(geom_it_id_aktuell_stat)+"','"+str(geom_part_id_aktuell_stat)+"','0')")

		cursor.execute("SELECT * FROM optimierungs_parameter")
		res_opt_param = cursor.fetchall()
		iob_name = res_opt_param[0]['iob_filename']
		pa_names = pickle.loads(res_opt_param[0]['PA_filenames'])
		vektor_fix_volt = pickle.loads(res_opt_param[0]['fix_voltages'])
		vektor_fix_elek_nr = pickle.loads(res_opt_param[0]['fix_electrodes'])
		anz_v_pro_pa = pickle.loads(res_opt_param[0]['anz_v_pro_pa'])
		cursor.execute("UPDATE status_r SET status = '1' WHERE R_id = '"+id_r_str+"'")
		datenbank.commit()
		datenbank.close()
		
		list_fix_volt = []
		list_fix_eleknr = []
		
		return new_gem_flag, geom_part_id_aktuell_stat, voltages_rueckgabe, iob_name, pa_names, vektor_fix_volt, vektor_fix_elek_nr, anz_v_pro_pa
	else:
		datenbank.commit ()
		datenbank.close ()
		return False
	

