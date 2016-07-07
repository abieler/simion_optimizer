import os, sys
import time
from glob import glob
from ftplib import FTP
from slave_funcs import *
from calculate_target_function import calculate_target_function

silent_remove("batchfile_log.log")
silent_remove("geometry_particle_history.log")
silent_remove("tf_control_file.txt")
silent_remove("tf_control.txt")

SIMION_PATH, SIMION_BIN = get_simion_settings()

print "START main loop on slave: ", myID
loop_counter = 0
while True:
    ##############################################################################
    #                           GET ALL INFOS FROM DATABASE                      #
    ##############################################################################
    for fileName in glob("optimizer_*_data.txt"):
        os.remove(fileName)
    #os.system('del optimizer_*_data.txt')
    refiner_list, gemfile_exists, gemfile_name, iob_filename = get_simion_files(FTP_IP, FTP_USER, FTP_PW)

    # reserve jobs
    X, volt_iteration = algo_param(myID, nCores)

    if volt_iteration == 1 or loop_counter == 0:
        print 'First voltage iteration!'
        if gemfile_exists:
            print 'found gemfile: %s' % gemfile_name
            pa_name = gemfile_name.split('.')[0] + '.pa#'
            os.system(SIMION_BIN + ' gem2pa %s %s' % (gemfile_name, pa_name))
            print 'converted gemfile to pa...'
            print SIMION_BIN + ' gem2pa %s %s' % (gemfile_name, pa_name)

        for filename in refiner_list:
            print SIMION_BIN + ' --nogui --noprompt refine ' + SIMION_PATH + filename[:-1] + '#"'
            os.system(SIMION_BIN + ' --nogui --noprompt refine ' + SIMION_PATH + filename[:-1] + '#"')
        loop_counter += 1

    ##############################################################################
    #                        FASTADJUST AN FLY IONS                              #
    ##############################################################################
    print 'FAST ADJUSTING ADJUSTABLE VOLTAGES AND FLY EM'
    for i in range(len(X)):
        fastadjust_adj_voltages_and_fly_ions(X[i], iob_filename,i)
        os.system('START /B ' + SIMION_BIN + ' --default-num-particles=60001 --nogui --noprompt lua start_simion_session_' + str(i) + '.lua >>nul')
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

    write_zielf(id_r, target_function)
