from __future__ import division
from numpy import std,mean,sqrt,exp
import time

def calculate_target_function(number_of_particles):
	target_function = []
	worst_target_function_value = 20
	for index in range(number_of_particles):
		TF = worst_target_function_value
		nr,tof,m,x,y,z,az,el,vx,vy,vz,ke = [], [], [], [], [], [], [], [], [], [], [], []
		nr_D,tof_D,m_D,x_D,y_D,z_D,az_D,el_D,vx_D,vy_D,vz_D,ke_D = [], [], [], [], [], [], [], [], [], [], [], []
		NR,TOF,M,X,Y,Z,AZ,EL,VX,VY,VZ,KE = 0,0,0,0,0,0,0,0,0,0,0,0

		try:
			file = open('optimizer_' + str(index) + '_data.txt','r')
			for line in file:
				try:
					NR,TOF,M,X,Y,Z,AZ,EL,VX,VY,VZ,KE = line.split(',')
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
					ke.append(float(KE))
				except:
					pass
				
			for NR,TOF,M,X,Y,Z,AZ,EL,VX,VY,VZ,KE in zip(nr,tof,m,x,y,z,az,el,vx,vy,vz,ke):
				try:
					#if (59.8 < X): # chims.iob
					if (X > 290): # einzel.iob
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
				transmission = 100.* len(y_D)/len(y)
				'''
				if len(y_D) > 10:
					resolution = mean(tof_D) / std(tof_D)
				else:
					resolution = 0.1
				'''
				
				footprint = (std(y_D) + std(z_D)) / (len(z_D)+0.001)
				#if(transmission <= 0.7):
				TF = -transmission / footprint
				#else:
					#TF = 5
			except Exception,e :
				TF = 123.456
				print e
				time.sleep(1)
				
			
			target_function.append(TF)
		

		except:
			target_function.append(worst_target_function_value)
			print 'could not open simion data file'
			goo = open('not_opened_files.log','a')
			goo.write('optimizer_' + str(index) + '_data.txt   ' + str(time.strftime('%d.%m.%Y  %H:%M:%S')) +'\n')
			goo.close()
			
	return target_function
