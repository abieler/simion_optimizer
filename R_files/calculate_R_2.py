import os, sys
import time
from ftplib import FTP
from calculate_R_functions import *
from calculate_target_function import calculate_target_function


os.system('del batchfile_log.log')
os.system('del geometry_particle_history.log')
os.system('del tf_control_file.txt')
os.system('del tf_control.txt')

loop_counter = 0
while True:
	##############################################################################
	#                           GET ALL INFOS FROM DATABASE                      #
	##############################################################################
	
	os.system('del optimizer_*_data.txt')
	refiner_list, gemfile_exists,gemfile_name,iob_filename = get_simion_files_2()
	
	# reserve jobs
	X, volt_iteration = get_algo_param_3(id_r,number_of_cores)
	
	if volt_iteration == 1 or loop_counter == 0:
		print 'First voltage iteration!'
		if gemfile_exists:
			print 'found gemfile: %s' % gemfile_name
			pa_name = gemfile_name.split('.')[0] + '.pa#'
			os.system('simion gem2pa %s %s'%(gemfile_name, pa_name))
			print 'converted gemfile to pa...'
			print 'simion gem2pa %s %s'%(gemfile_name, pa_name)
			
		for filename in refiner_list:
			print 'simion --nogui --noprompt refine ' + simion_dir + filename[:-1] + '#"'
			#os.system('simion --nogui --noprompt refine ' + simion_dir + filename[:-1] + '#"')
		loop_counter += 1
	##############################################################################
	#                        FASTADJUST AN FLY IONS                              #
	##############################################################################
	

	print 'FAST ADJUSTING ADJUSTABLE VOLTAGES AND FLY EM'
	#fastadjust_adj_voltages_and_fly_ions_2(X,iob_filename)
	for i in range(len(X)):
		fastadjust_adj_voltages_and_fly_ions_2(X[i],iob_filename,i)
		os.system('START /B simion --default-num-particles=60001 --nogui --noprompt lua start_simion_session_' + str(i) + '.lua >>nul')
	time.sleep(0.2)
	
	print 'waiting for simulations to end...'
	while True:
		sum_flags = 0
		for i in range(len(X)):
			try:
				f = open('finished_' + str(i) + '.txt')
				sum_flags += int(f.readline()[0])
			except:
				pass
				#print 'could not load : ' + 'finished_' + str(i) + '.txt'
		if sum_flags == len(X):
			break
		time.sleep(0.2)
	
	for i in range(len(X)):
		os.system('echo 0 >finished_' + str(i) + '.txt ')
	###############################################################################


	target_function = calculate_target_function(len(X))
	print target_function
	print len(target_function)
	
	
	write_zielf(id_r,target_function)
			
