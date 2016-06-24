from __future__ import division
from numpy import std,mean,sqrt,exp,array,arccos,dot,pi
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
                    #if (X > 178.5 and phi <= 2.1 and (Y**2 + Z**2 < 0.564)): # dotsXS_3.iob
                    #if (X > 178.5): # dots.iob
                    if (X > 78): # example.iob
                    #if (X > 499.5 and -60 < Y < 60): # einzel.iob

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

                footprint = sqrt(sum(array(y_D)**2 + array(z_D)**2)) + 1

                TF = -transmission

            except Exception, e:
                TF = 666666666
                print e


            target_function.append(TF)

        except:
            target_function.append(worst_target_function_value)
            print 'could not open simion data file'
            goo = open('not_opened_files.log','a')
            goo.write('optimizer_' + str(index) + '_data.txt   ' + str(time.strftime('%d.%m.%Y  %H:%M:%S')) +'\n')
            goo.close()

    return target_function
