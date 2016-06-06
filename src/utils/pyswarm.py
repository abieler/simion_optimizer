from __future__ import division
import numpy as np
from matplotlib.pyplot import figure,plot,show,semilogy,ion


def evaluate_evolution_state(X,jackpot_index,previous_state,best_point):
    d =[np.sqrt(np.sum((xi-X)**2)) for xi in X ]                                #di = die distanz des particles i zu allen anderen particles

    #dg = sqrt(sum((best_point-X)**2))
    
    #d[jackpot_index] = dg
    dg = d[jackpot_index]                                               #dg = die distanz des global besten particles zu allen anderen

    f = (dg - np.array(d).min()) / (np.array(d).max() - np.array(d).min())                              # f = evolutionary factor [0...1]
    #berechne jetzt aus f in welchem stadium s1, s2, s3 oder s4 sich der swarm befindet. fuzzy style.
    try:
        if 0 <= f <= 0.4:                                                   # mu_s1 = gewichtungsfaktor zum stadium S1 (exploration)
            mu_s1 = 0
        elif 0.4 < f <= 0.6:
            mu_s1 = 5*f-2
        elif 0.6 < f <= 0.7:
            mu_s1 = 1
        elif 0.7 < f <= 0.8:
            mu_s1 = -10*f+8
        elif 0.8 < f <= 1:
            mu_s1 = 0
            
        if 0 <= f <= 0.2:                                                   # mu_s2 = gewichtungsfaktor zum stadium S2 (explotation)
            mu_s2 = 0
        elif 0.2 < f <= 0.3:
            mu_s2 = 10*f-2
        elif 0.3 < f <= 0.4:
            mu_s2 = 1
        elif 0.4 < f <= 0.6:
            mu_s2 = -5*f+3
        elif 0.6 < f <= 1:
            mu_s2 = 0
            
        if 0 <= f < 0.1:                                                    # mu_s3 = gewichtungsfaktor zum stadium S3 (convergence)
            mu_s3 = 1                                                       
        elif 0.1 < f <= 0.3:
            mu_s3 = -5*f+1.5
        elif 0.3 < f <= 1:
            mu_s3 = 0
        
        
        if 0 <= f < 0.7:                                                    # mu_s4 = gewichtungsfaktor zum stadium S4 (jumping out)
            mu_s4 = 0
        elif 0.7 < f <= 0.9:
            mu_s4 = 5*f-3.5
        elif 0.9 < f <= 1:
            mu_s4 = 1
    
        
        mu = [None,mu_s1, mu_s2, mu_s3, mu_s4]                              # das dummy-element none ist nur da, damit die indices von mu mit den stadien uebereinstimmen.
    
    except:
        print '********************************************'
        print 'iteration = ' +str(iteration)
        print 'f = ' + str(f)
        print 'dg  = ' + str(dg)
        print 'array(d).min() = ' + str(np.array(d).min())
        print 'array(d).max() = ' + str(np.array(d).max())
        for xx in X:
            print xx
        print d
        print '*********************************************'
                                                                        # mu[1] gehoert dann zu s1!
    best_mu = mu.index(np.array(mu).max())                              #findet den index des groessten mu_i


    if not previous_state:
        current_state = best_mu
        
    elif previous_state == 1:                                               
        if mu[1] > 0:                               #bleib im gleichen stadium falls mu_s1 > 0
            current_state = 1
        else:                                       #falls mu_s1 == 0 schau ob mu_s2 oder mu_s4 > 0 sind. Wenn ja, dann waehle einen von diesen
            if mu[2] > 0:                           #stadien aus. (mu_s2 und mu_s4 koennen nicht gleichzeitig > 0 sein!)
                current_state = 2
            elif mu[4] > 0:
                current_state = 4
            else:
                current_state = 3
    elif previous_state == 2:
        if mu[2] > 0:
            current_state = 2
        else:
            if mu[3] > 0:
                current_state = 3
            elif mu[1] > 0:
                current_state = 1
            else:
                current_state = 4
    elif previous_state == 3:
        if mu[3] > 0:
            current_state = 3
        else: 
            if mu[4] > 0:
                current_state = 4
            elif mu[2] > 0:
                current_state = 2
            else:
                current_state = 1
    elif previous_state == 4:
        if mu[4] > 0:
            current_state = 4
        else:
            if mu[1] > 0:
                current_state = 1
            elif mu[2] > 0:
                current_state = 2
            else:
                current_state = 3
    
    
    return current_state,f



def apsa(func,x0,xmin=None,xmax=None,dx=None,number_of_particles=None,max_iterations=None,cluster_extension = False):
    
    '''
    Optimize function f with adaptive particle swarm optimization method
    
    f:  callable function from user. this function has to return the value of the target function.
    x0: starting point for optimization (array)
    dx: delta values for first population
    xmin/xmax: array for search space, minimum and maximum for every parameter to optimize
    nr_of_particles: swarm size
    max_iterations: optimization stops after max_iterations
    '''
    #print 'xmin = ' + str(xmin)
    #print 'xmax = ' + str(xmax)
    
    x0 = np.array([xx for xx in x0])
    
    if dx == None:
        dx = np.array([2*abs(xx) for xx in x0])
    else:
        dx = np.array([xx for xx in dx])
        
    if xmin == None:
        xmin = []
        for xx,ddx in zip(x0,dx):
            xmin.append(xx-ddx)
        xmin = np.array(xmin)
    else:
        xmin = np.array([xx for xx in xmin])
        
        
    if xmax == None:
        xmax = []
        for xx,ddx in zip(x0,dx):
            xmax.append(xx+ddx)
        xmax = np.array(xmax)
    else:
        xmax = np.array([xx for xx in xmax])
        
    if number_of_particles == None:
        number_of_particles = len(x0)
    else:
        number_of_particles = int(number_of_particles)
        
    if max_iterations == None:
        max_iterations = 150 * len(x0)
    else:
        max_iterations = int(max_iterations)
        
    
    #print 'xmin = ' + str(xmin)
    #print 'xmax = ' + str(xmax)
    
    
    c1 = 2.0
    c2 = 2.0
    w = 0.9

    R1 = np.random.uniform(-1,1,[number_of_particles, len(x0)])
    R2 = np.random.uniform(-1,1,[number_of_particles, len(x0)])
    X0 = np.ones([number_of_particles, len(x0)]) * x0
    DX = np.ones([number_of_particles,len(x0)]) * dx
    V = np.ones([number_of_particles,len(x0)]) * dx * np.random.uniform(-1,1,[number_of_particles, len(x0)])

    #X = X0 + R1*DX
    
    X = np.random.uniform(xmin,xmax,[number_of_particles,len(x0)])
    X[0] = x0
    
    '''
    print 'Elements of X are:'
    for xxxx in X:
        print xxxx
        
    raw_input()
    '''
    
    iteration = 0
    
    found_maximum = False
    found_maximum_random = False
    current_state = None
    
    best_tf_value_global = 100
    
    tf_history = []
    tf_mean_history = []
    ion()
    while iteration <= max_iterations:
        
        ###########################################
        # limit all voltages according to xmin and xmax
        ##############################################

        for p_index in range(0,number_of_particles):        #p_index = particle index, v_index = voltage index
            for v_index in range(0,len(x0)):
                if X[p_index][v_index] < xmin[v_index]:
                    X[p_index][v_index] = xmin[v_index] + np.random.uniform(0,0.01)*xmin[v_index]
                elif X[p_index][v_index] > xmax[v_index]:
                    X[p_index][v_index] = xmax[v_index] - np.random.uniform(0,0.01)*xmax[v_index]


        ########################################################################
        ##                      SWARM ALGORITHM                             ####
        ########################################################################
        if cluster_extension:
            tf = func(X)
        else:
            tf = []
            for x in X:
                TF = func(x)
                tf.append(TF)

            

        if iteration == 0:
            best_tf_value_global = min(tf)
            tf_best = [x for x in tf]
            X_best = [x for x in X]
        
            best_tf_value_global = min(tf)
            try:
                if len(best_tf_value_global) > 1:
                    best_tf_value_global = best_tf_value_global[0]
            except:
                pass
            
        worst_tf_value_global = max(tf)
        
        
        j = 0
        for value,value_best in zip(tf,tf_best):
            if value <= value_best:
                tf_best[j] = value
                X_best[j] = X[j]
                        
                if value <= best_tf_value_global:
                    best_point = [x for x in X[j]]
                    best_tf_value_global = value
                    jackpot_index = j
            if value == worst_tf_value_global:
                    loser_index = j
            j += 1
            
            
        if cluster_extension:
            pass
        else:
            #########################################################################################
            # Elitist learning: Take the worst particle and replace it with x_learn.
            # x_learn is like the best particle but in one dimension it is changed by a random value.
            #########################################################################################


            random_index = np.random.randint(0,len(x0))
            random_value = np.random.normal(-1,1)
            x_learn = np.array([x for x in best_point])
            sigma_learn = 1 - (1 - 0.1) * iteration / max_iterations
            
            x_learn[random_index] = x_learn[random_index] + (xmax[random_index] - xmin[random_index])/3 * np.random.normal(0,sigma_learn)
            
            if x_learn[random_index] < xmin[random_index]:
                x_learn[random_index] = xmin[random_index]
            elif x_learn[random_index] > xmax[random_index]:
                x_learn[random_index] = xmax[random_index]
                
                
            ##########################################################################################
            # elitist learning
            ##########################################################################################

            tf_x_learn = func(x_learn)
            
            
            if tf_x_learn < best_tf_value_global:
                X[jackpot_index] = [x for x in x_learn]
                X_best[jackpot_index] = [x for x in x_learn]
                tf_best[jackpot_index] = tf_x_learn
                tf[jackpot_index] = tf_x_learn
                best_point = [x for x in x_learn]
                best_tf_value_global = tf_x_learn

        
        current_state,f = evaluate_evolution_state(X,jackpot_index,current_state,best_point)
        
        delta_c1 = np.random.uniform(0.05,0.1)
        delta_c2 = np.random.uniform(0.05,0.1)

        if current_state == 1:
            c1 += delta_c1
            c2 -= delta_c2
        elif current_state == 2:
            c1 += delta_c1/2
            c2 -= delta_c2/2
        elif current_state == 3:
            c1 += delta_c1/2
            c2 += delta_c2/2
        elif current_state == 4:
            c1 -= delta_c1
            c2 += delta_c2
            
        if c1 < 1.5:
            c1 = 1.5
        if c1 > 2.5:
            c1 = 2.5
        if c2 < 1.5:
            c2 = 1.5
        if c2 > 2.5:
            c2 = 2.5
            
        if c1+c2 > 4:
            c_total = c1+c2
            c1 = c1/c_total*4
            c2 = c2/c_total*4
        
        w = 1/(1+1.5*np.exp(-2.6*f))
        

        ## berechne VX und VG fuer die naechste swarm position
        VX = X_best - X
        VG = best_point - X
        r1 = np.random.uniform(0,1,[number_of_particles,np.shape(X)[1]])
        r2 = np.random.uniform(0,1,[number_of_particles,np.shape(X)[1]])
        
        
        V_new = V*w + c1 * r1 * VX + c2 * r2 * VG
        V = V_new
                    
        X_new = X + V
        X = X_new
        
        iteration += 1
        
        print best_tf_value_global
        tf_history.append(best_tf_value_global)
        tf_mean_history.append(np.mean(tf))
        
        
        
        '''
        if iteration %25 == 0:
            figure(1)
            semilogy(tf_history)
            semilogy(tf_mean_history)
            show()
        '''
        
    return best_tf_value_global,best_point
        
