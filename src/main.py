'''
COMMAND TO GENERATE NEW PYTHON MODULE FROM QT DESIGNER .ui FILE:
pyuic4 -o ui_optimizer.py optimizer.ui
'''

from __future__ import division
import PyQt4.QtCore as QTC
import PyQt4.QtGui as QTG
from numpy import random,array
import sys
import time
import os

import gui.ui_simion_optimizer as ui_simion_optimizer
from utils.pyswarm import apsa
from utils.mysql_funcs import *
from utils.io import write_lua_file, import_gemfile
from utils.gemfile_creator import create_gemfile


class Window(QTG.QWidget,ui_simion_optimizer.Ui_Form):

    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setupUi(self)                          # builtin function to build the GUI from the ui_*.py module
        self.setWindowTitle('SIMION OPTIMIZER')
        self.optimizer_thread = Optimizer()
        
        self.connect(self.pushButton_start,QTC.SIGNAL("clicked()"),self.start_button_clicked)
        self.connect(self.pushButton_stop,QTC.SIGNAL("clicked()"),self.stop_button_clicked)
        self.connect(self.pushButton_load_gemfile,QTC.SIGNAL("clicked()"),self.load_gemfile_clicked)
        
        ####################################################################
        # read simion directory and fill comboboxes with pa and iob names
        ####################################################################
        #self.path_simion = '/home/hs/ftp/'
        self.path_simion = os.path.join("..", "input") 
        files = os.listdir(self.path_simion)
        files.sort()
        pas_in_directory = []
        iob_filename = None
        
        self.comboBox_pa1.addItem('---')
        self.comboBox_pa2.addItem('---')
        self.comboBox_pa3.addItem('---')
        self.comboBox_iob.addItem('---')

        for file in files:
            if file[-1] == '#':
                self.comboBox_pa1.addItem(file)
                self.comboBox_pa2.addItem(file)
                self.comboBox_pa3.addItem(file)
            elif file.split('.')[-1] == 'iob':
                self.comboBox_iob.addItem(file)
            elif file.split('.')[-1] == 'opt':
                self.comboBox_load.addItem(file)
        
        
    def load_gemfile_clicked(self):
        gem_filename = str(self.comboBox_iob.currentText()).split('.')[0] + '.gem'
        print gem_filename
        import_gemfile(gem_filename,[1,2,3])

        
    def start_button_clicked(self):
        self.optimizer_thread.start()
    

    def stop_button_clicked(self):
        pass
        
        
class Optimizer(QTC.QThread):

    def __init__(self, parent = None):
        QTC.QThread.__init__(self,parent)
        

    def __del__(self):
        self.exiting = True
        
        
    def evaluation_function(self,X):
        ################################################
        # write voltages and algorithm parameters into
        # the database so that working nodes can access
        # this data.
        ################################################
        write_algo_parameters_to_db_2(X,self.geom_iteration_counter,self.geom_particle_counter)
        
        ################################################
        # wait for Rs to calculate target functions
        ################################################
        dont_have_target_function = True
        print 'waiting to recieve target functions from R'
        t0 = time.time()
        while dont_have_target_function:
            target_function = get_target_functions_from_db(len(X))
            if len(target_function) == len(X):
                dont_have_target_function = False
                target_function.reverse()
                print target_function
                #raw_input()
                return target_function
            else:
                time.sleep(1)
            print target_function
            print random.uniform(0,1)
    
        
    def voltage_optimization(self,G):
        
        ################################################################
        # comment the following line if you do a voltage optimization!!!
        ################################################################
        if window.checkBox_voltage_only.isChecked():
            pass
        else:
            create_gemfile(G)
        
        ################################################################
        # do not comment anything below here!
        ################################################################
        tf_best, best_voltages = apsa(self.evaluation_function,
                                      self.x0,
                                      self.vmin,
                                      self.vmax,
                                      None,
                                      self.number_of_particles,
                                      self.max_number_of_voltage_iterations,
                                      True)
        
        self.super_counter += 1
        self.geom_particle_counter += 1

        if self.super_counter == self.nr_of_geom_particles:
            self.super_counter = 0
            self.geom_iteration_counter += 1
            self.geom_particle_counter = 0
            
        print 'Voltage optimization finished!'
        print tf_best
        file = open('./optimized_data.txt','a')
        file.write(window.comboBox_iob.currentText() + '\n')
        file.write('Fitness Function Value: %f\n' %tf_best)
        file.write('Voltage Values: ')
        for volt in best_voltages:
            file.write(str(volt) +', ' )
        file.write('\n')
        file.write('Geometry Parameters: ')
        for g in G:
            file.write('%f,' %g)
        file.write('\n')
        file.write('**'*10 + '\n')
        file.close()
        return tf_best

        
    def run(self):
        print 'optimizing!'
        
        database = mysql_connect()
        database.query("TRUNCATE TABLE jobs")
        database.query("TRUNCATE TABLE voltages")
        database.commit()
        database.close()
        
        self.super_counter = 0
        self.geom_iteration_counter = 0
        self.geom_particle_counter = 0
        
        ####################################################################
        #                   GET USER PARAMETERS                            #
        ####################################################################
        
        adj_elec_pa1 = []
        adj_elec_pa2 = []
        adj_elec_pa3 = []
        
        adj_volt_pa1 = []
        adj_volt_pa2 = []
        adj_volt_pa3 = []
        
        delta_v_pa1 = []
        delta_v_pa2 = []
        delta_v_pa3 = []
        
        fix_elec_pa1 = []
        fix_elec_pa2 = []
        fix_elec_pa3 = []
        
        fix_volt_pa1 = []
        fix_volt_pa2 = []
        fix_volt_pa3 = []
        
        vmin_pa1 = []
        vmin_pa2 = []
        vmin_pa3 = []
        
        vmax_pa1 = []
        vmax_pa2 = []
        vmax_pa3 = []
        
        try:
            adj_elec_pa1 = [int(v) for v in window.textEdit_adj_elec_pa1.toPlainText().split('\n')]
            adj_elec_pa2 = [int(v) for v in window.textEdit_adj_elec_pa2.toPlainText().split('\n')]
            adj_elec_pa3 = [int(v) for v in window.textEdit_adj_elec_pa3.toPlainText().split('\n')]
        except:
            pass
        
        try:
            adj_volt_pa1 = [float(v) for v in window.textEdit_adj_volt_pa1.toPlainText().split('\n')]
            adj_volt_pa2 = [float(v) for v in window.textEdit_adj_volt_pa2.toPlainText().split('\n')]
            adj_volt_pa3 = [float(v) for v in window.textEdit_adj_volt_pa3.toPlainText().split('\n')]
        except:
            pass
        
        try:
            vmin_pa1 = [float(v) for v in window.textEdit_v_min_pa1.toPlainText().split('\n')]
            vmin_pa2 = [float(v) for v in window.textEdit_v_min_pa2.toPlainText().split('\n')]
            vmin_pa3 = [float(v) for v in window.textEdit_v_min_pa3.toPlainText().split('\n')]
        except:
            pass
        try:
            
            vmax_pa1 = [float(v) for v in window.textEdit_v_max_pa1.toPlainText().split('\n')]
            vmax_pa2 = [float(v) for v in window.textEdit_v_max_pa2.toPlainText().split('\n')]
            vmax_pa3 = [float(v) for v in window.textEdit_v_max_pa3.toPlainText().split('\n')]
        except:
            pass
        
        try:
            fix_elec_pa1 = [int(v) for v in window.textEdit_fix_elec_pa1.toPlainText().split('\n')]     
            fix_elec_pa2 = [int(v) for v in window.textEdit_fix_elec_pa2.toPlainText().split('\n')]     
            fix_elec_pa3 = [int(v) for v in window.textEdit_fix_elec_pa3.toPlainText().split('\n')]
        except:
            pass
        
        try:
            fix_volt_pa1 = [float(v) for v in window.textEdit_fix_volt_pa1.toPlainText().split('\n')]       
            fix_volt_pa2 = [float(v) for v in window.textEdit_fix_volt_pa3.toPlainText().split('\n')]       
            fix_volt_pa3 = [float(v) for v in window.textEdit_fix_volt_pa3.toPlainText().split('\n')]
        except:
            pass
            
        fix_voltages = [fix_volt_pa1, fix_volt_pa2, fix_volt_pa3]
        fix_electrodes = [fix_elec_pa1, fix_elec_pa2, fix_elec_pa3]
        self.vmin = vmin_pa1 + vmin_pa2 + vmin_pa3
        self.vmax = vmax_pa1 + vmax_pa2 + vmax_pa3
        self.x0 = adj_volt_pa1 + adj_volt_pa2 + adj_volt_pa3
        
        print 'Starting values for optimization:'
        
        for valuee in self.x0:
            print valuee
        
        ###########################################################
        # check if just voltage optimization is needed
        ###########################################################
        use_voltage_only = window.checkBox_voltage_only.isChecked()
    
        self.number_of_particles = int(window.lineEdit_particles.text())
        self.max_number_of_voltage_iterations = int(window.lineEdit_iterations.text())
        number_of_bad_news = int(window.lineEdit_bad_news.text())
        anz_v_pro_pa = [len(adj_elec_pa1), len(adj_elec_pa2), len(adj_elec_pa3)]
        
        iob_filename = str(window.comboBox_iob.currentText())
        print 'iob Filename: ', iob_filename
        pa1_filename = str(window.comboBox_pa1.currentText())
        pa2_filename = str(window.comboBox_pa2.currentText())
        pa3_filename = str(window.comboBox_pa3.currentText())
        
        PA_filenames = [pa1_filename, pa2_filename, pa3_filename]
        PA_filenames = [paname for paname in PA_filenames if '---' not in paname]
        print 'PA Filenames: ', PA_filenames
        
        try:
            leader_electrode_1 = int(window.lineEdit_leader1.text())
            disciple_electrodes_1 = [float(v) for v in window.textEdit_disciples1.toPlainText().split('\n')]
        except:
            leader_electrode_1 = None
            disciple_electrodes_1 = None
        try:
            leader_electrode_2 = int(window.lineEdit_leader2.text())
            disciple_electrodes_2 = [float(v) for v in window.textEdit_disciples2.toPlainText().split('\n')]
        except:
            leader_electrode_2 = None
            disciple_electrodes_2 = None
        try:
            leader_electrode_3 = int(window.lineEdit_leader3.text())
            disciple_electrodes_3 = [float(v) for v in window.textEdit_disciples3.toPlainText().split('\n')]
        except:
            leader_electrode_3 = None
            disciple_electrodes_3 = None
        leader_electrodes = [leader_electrode_1,leader_electrode_2,leader_electrode_3]
        disciple_electrodes = [disciple_electrodes_1,disciple_electrodes_2,disciple_electrodes_3]
        
        use_voltage_only = window.checkBox_voltage_only.isChecked()
        
        number_of_bad_news = 1111
        bad_news_difference = 0.0001
        number_of_geom_particles = 1
        
        if True:#use_voltage_only == False:
            self.nr_of_geom_particles = int(window.lineEdit_nr_of_g_particles.text())
            self.nr_of_geom_iterations = int(window.lineEdit_nr_of_g_iterations.text())
            self.G = [float(v) for v in window.textEdit_g.toPlainText().split('\n')]
            self.gmin = [float(v) for v in window.textEdit_g_min.toPlainText().split('\n')]
            self.gmax = [float(v) for v in window.textEdit_g_max.toPlainText().split('\n')]
            
        print 'init optimizer db'
        init_optimizer_db(number_of_bad_news,bad_news_difference,self.number_of_particles,self.max_number_of_voltage_iterations,anz_v_pro_pa,fix_voltages,fix_electrodes,iob_filename,PA_filenames,self.nr_of_geom_particles)
        print 'init db finished'
        write_lua_file(adj_elec_pa1,
                       adj_elec_pa2,
                       adj_elec_pa3,
                       fix_elec_pa1,
                       fix_elec_pa2,
                       fix_elec_pa3,
                       fix_volt_pa1,
                       fix_volt_pa2,
                       fix_volt_pa3,
                       iob_filename,
                       PA_filenames,
                       window.path_simion)
        
        cluster_extension = True
        if use_voltage_only == True:
            print 'voltage optimization'
            print 'Press Enter to continue...'
            raw_input()
            self.voltage_optimization([0])
            #apsa(self.evaluation_function,x0,vmin,vmax,number_of_particles=number_of_particles,max_iterations=max_number_of_voltage_iterations,cluster_extension = True)
        else:
            print 'geometry optimization'
            #print self.gmin
            #print self.gmax
            
            #raw_input()
            apsa(self.voltage_optimization,self.G,xmin=self.gmin,xmax=self.gmax,number_of_particles=self.nr_of_geom_particles)
            
            #self.voltage_optimization(g,)
            #apsa(self.evaluation_function,x0,vmin,vmax,number_of_particles=number_of_particles,max_number_of_voltage_iterations,cluster_extension)
            
        
app = QTG.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
