import sys
import time
import pickle
from MySQLdb import *


def mysql_connect():
    host_var = 'localhost'
    user_var = 'root'
    pw_var = 'jd7he65'
    db_var = 'simion_optimizer_db'

    try:
        verb = connect(host=host_var,user=user_var,db=db_var,passwd=pw_var)
        return verb
    except Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit()

def write_zielf(id_r,part_volt_id,zielf):
    id_r_str = str(id_r)
    datenbank = mysql_connect()
    cursor = datenbank.cursor (cursors.DictCursor)
    cursor.execute ("UPDATE jobs SET zielfunktion = '"+str(zielf)+"', status = '2' WHERE status = '1' AND part_volt_id = '"+str(part_volt_id)+"' LIMIT 1")
    datenbank.commit ()
    datenbank.close ()
    return True



def get_zielf_w_ready(): #gibt eine liste mit allen zielfunktionen oder false zurueck
    datenbank = mysql_connect()
    cursor = datenbank.cursor (cursors.DictCursor)
    cursor.execute ("SELECT status FROM jobs WHERE status != '2'")
    rows = cursor.rowcount
    if rows == 0: #schauen ob alle fertig sind, wenn einer nicht status 2 hat ist er nicht fertig
        cursor.execute ("SELECT zielfunktion FROM jobs ORDER BY part_volt_id ASC")
        result_set = cursor.fetchall()
        zielffunk_list = []
        for key in result_set:
            zielffunk_list.append(key['zielfunktion'])
        cursor.execute ("TRUNCATE TABLE jobs")
        cursor.execute ("TRUNCATE TABLE voltages")
        datenbank.commit ()
        datenbank.close ()
        return zielffunk_list
    else:
        datenbank.close ()
        return False

def init_optimizer_db(number_of_bad_news,bad_news_difference,number_of_particles,max_number_of_voltage_iterations,anz_v_pro_pa,fix_voltages,fix_electrodes,iob_filename,PA_filenames,number_of_geom_particles=1):
    datenbank = mysql_connect()
    cursor = datenbank.cursor (cursors.DictCursor)
    cursor.execute("TRUNCATE TABLE optimierungs_parameter")
    cursor.execute("TRUNCATE TABLE jobs")
    cursor.execute("TRUNCATE TABLE voltages")
    cursor.execute("TRUNCATE TABLE best_values")
    cursor.execute("TRUNCATE TABLE status_r")
    cursor.execute("TRUNCATE TABLE status_of_gem_particle")
    anz_v_pro_pa_serialized = pickle.dumps(anz_v_pro_pa)
    fix_voltages_serialized = pickle.dumps(fix_voltages)
    fix_electrodes_serialized = pickle.dumps(fix_electrodes)
    PA_filenames_serialized = pickle.dumps(PA_filenames)
    #if(number_of_geom_particles == 0):
    #   number_of_geom_particles = 1

    cursor.execute("INSERT INTO optimierungs_parameter (anzahl_bad_news, max_diff_bad_news, anzahl_geom_part,anzahl_volt_part,max_volt_iterations,anz_v_pro_pa,fix_voltages,fix_electrodes,iob_filename,PA_filenames) VALUES ('"+str(number_of_bad_news)+"','"+str(bad_news_difference)+"','"+str(number_of_geom_particles)+"','"+str(number_of_particles)+"','"+str(max_number_of_voltage_iterations)+"',\""+str(anz_v_pro_pa_serialized)+"\",\""+str(fix_voltages_serialized)+"\",\""+str(fix_electrodes_serialized)+"\",'"+str(iob_filename)+"',\""+str(PA_filenames_serialized)+"\")")

    datenbank.commit()
    datenbank.close()


def write_algo_parameters_to_db(arr_voltages,geom_it_id=0,geom_part_id=0):
    datenbank = mysql_connect()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor = datenbank.cursor (cursors.DictCursor)
    cursor.execute("SELECT MAX(volt_it_id) AS act_volt_it_id FROM jobs WHERE geom_it_id = '"+str(geom_it_id)+"' AND geom_part_id = '"+str(geom_part_id)+"'")
    result_set = cursor.fetchall()
    if(result_set[0]['act_volt_it_id'] == None):
        result_set[0]['act_volt_it_id'] = 0
    voltage_it_id = result_set[0]['act_volt_it_id'] + 1

    cursor.execute("SELECT MAX(job_id) FROM jobs")
    db_data = cursor.fetchall()
    try:
        current_job = int(db_data[0]["MAX(job_id)"])+1
    except:
        current_job = 1
    print 'current_job = '
    print current_job

    i=0
    query_string_tmp = "INSERT INTO voltages (job_id,geom_iteration_id,geom_particle_id,voltage_iteration_id,voltage_particle_id,volt_id,voltage,v) VALUES "
    for X in arr_voltages:
        k=0
        datenbank.query("INSERT INTO jobs (geom_it_id,geom_part_id,volt_it_id,part_volt_id,datetime) VALUES ('"+str(geom_it_id)+"','"+str(geom_part_id)+"','"+str(voltage_it_id)+"','"+str(i)+"','"+str(timestamp)+"')")

        for X_sub in X:
            query_string_tmp += "('"+str(current_job+i)+"','"+str(geom_it_id)+"','"+str(geom_part_id)+"','"+str(voltage_it_id)+"','"+str(i)+"','"+str(k)+"','"+str(X_sub)+"','"+str(0)+"'),"
            k+=1
        print current_job+i
        i+=1
    query_string = query_string_tmp[:-1]


    datenbank.query(query_string)


def write_zielf_g(id_r,zielf): #zielf ist eine list mit den zielfunktionen in der richtigen reihenfolge
    id_r_str = str(id_r)
    datenbank = mysql_connect()
    cursor = datenbank.cursor (cursors.DictCursor)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute ("SELECT job_id FROM jobs WHERE id_R = '"+id_r_str+"' AND status = '1' ORDER BY part_volt_id")
    result_set = cursor.fetchall()

    i=0
    for key in result_set:
        job_id_tmp = key['job_id']
        cursor.execute ("UPDATE jobs SET zielfunktion = '"+str(zielf[i])+"', status = '2',datetime = '"+str(timestamp)+"' WHERE status = '1' AND job_id = '"+str(job_id_tmp)+"' LIMIT 1")
        i+=1
    datenbank.commit ()
    datenbank.close ()
    return True


########################################################################
########################################################################
#Zielfunktionen wenn eine Geometrieiteration durch ist
def get_zielf_w_ready_g(only_g_particles=0): #gibt eine liste mit allen zielfunktionen oder false zurueck
    datenbank = mysql_connect()
    cursor = datenbank.cursor (cursors.DictCursor)

    #zuerst schauen ob eine geometrie fertig ist
    cursor.execute("SELECT * FROM optimierungs_parameter")
    result_set = cursor.fetchall()
    anzahl_bad_news = result_set[0]['anzahl_bad_news'] #wie viele male darf es keine oder eine zu kleine verbesserung geben
    max_diff_bad_news = result_set[0]['max_diff_bad_news'] #wie gross muss der unterschied zw zwei tf's mindestens sein um NICHT bad news zu sein
    anzahl_geom_part = result_set[0]['anzahl_geom_part']
    anzahl_volt_part = result_set[0]['anzahl_volt_part']
    max_volt_iterations = result_set[0]['max_volt_iterations']

    cursor.execute("SELECT MAX(geom_it_id) AS act_geom_it FROM jobs")
    result_set = cursor.fetchall()
    geom_iteration = result_set[0]['act_geom_it']
    kompl_status = 2 * anzahl_volt_part * max_volt_iterations #status muss bei allen volt teilchen bei allen interationen auf 2 sein

    ####################################################################
    #dieses query holt die beste zielfunktion pro geometrie, wenn die voltage optimierung ins max voltages iteration limit gekommen ist
    #es gibt also nachher eine liste mit allen geometrieteilchen die fertig sind (voltage limit NICHT bad news) und
    #dazugehoerige zilefunktionen
    cursor.execute("SELECT MIN(zielfunktion) AS best_geom_tf, geom_part_id FROM jobs WHERE jobs.geom_it_id = '"+str(geom_iteration)+"' GROUP BY geom_part_id HAVING SUM(status) = '"+str(kompl_status)+"'")
    result_set = cursor.fetchall()
    geometry_particles_pronto = []
    geometry_tfs = []
    for key in result_set:
        geometry_particles_pronto.append(key['geom_part_id'])
        geometry_tfs.append(key['best_geom_tf'])

    ####################################################################
    #status muss bei allen volt teilchen bei allen interationen auf 2 sein
    #fuer den normalen abbruch
    kompl_status = 2 * anzahl_volt_part * max_volt_iterations
    tfs_all = []
    #bad news fertig

    cursor.execute("SELECT anzahl_geom_part FROM optimierungs_parameter")
    result_set = cursor.fetchall()
    anz_geom_parti_in_this_opti = result_set[0]['anzahl_geom_part']

    bad_news = zeros(anz_geom_parti_in_this_opti)
    bad_news_exp = zeros(anz_geom_parti_in_this_opti)
    #print result_set[0]
    #print 'bad_news = ' + str(bad_news)

    cursor.execute("SELECT MIN(zielfunktion) AS tf,geom_part_id,volt_it_id FROM jobs WHERE jobs.geom_it_id = '"+str(geom_iteration)+"' AND status = '2' GROUP BY geom_part_id,volt_it_id")
    result_set = cursor.fetchall()
    ref_setzen = True
    geom_part_id_old = -1
    for key in result_set:

        geom_part_id_aktuell = key['geom_part_id']
        if(geom_part_id_aktuell != geom_part_id_old):
            ref_setzen = True
            #bad_news.append(0)
            #bad_news_exp.append(0)
        if(ref_setzen):
            referenz_tf = key['tf']
            ref_setzen = False
        if(referenz_tf - key['tf'] > max_diff_bad_news and referenz_tf > key['tf']):
            bad_news[geom_part_id_aktuell] = 0
            bad_news_exp[geom_part_id_aktuell] -= 5
            referenz_tf = key['tf']
        else:
            bad_news[geom_part_id_aktuell] += 1
            bad_news_exp[geom_part_id_aktuell] += 1
        if(bad_news[geom_part_id_aktuell] < 0):
            bad_news[geom_part_id_aktuell] = 0
        if(bad_news_exp[geom_part_id_aktuell] < 0):
            bad_news_exp[geom_part_id_aktuell] = 0


        if(bad_news[geom_part_id_aktuell] == anzahl_bad_news):

            if(geometry_particles_pronto.count(geom_part_id_aktuell) == 0): #diese geom_part_id kommt schon vor, dieses teilchen wurde also durch max geom int beendet
                geometry_particles_pronto.append(geom_part_id_aktuell)

        geom_part_id_old = geom_part_id_aktuell

    if(only_g_particles == 1):
        return geometry_particles_pronto,geom_iteration,bad_news,bad_news_exp

    ###########################################################################################################
    #########               KOMPLETTE GEOMETRIE ITERATION FERTIG   ############################################
    ###########################################################################################################
    if(len(geometry_particles_pronto) == anzahl_geom_part):
        #die beste zielfunktion pro geometrie particle zurueckgeben
        cursor.execute("UPDATE status_of_gem_particle SET status = '1' WHERE geom_it_id = '"+str(geom_iteration)+"'");

        geometry_last_tf_per_particle = []
        geometry_best_tf_per_particle = []
        cursor.execute("SELECT MIN(zielfunktion) AS best_geometry_tf FROM jobs GROUP BY jobs.geom_part_id")
        result_set = cursor.fetchall()
        for key in result_set:
            geometry_best_tf_per_particle.append(key['best_geometry_tf'])

        cursor.execute("SELECT MIN(zielfunktion) AS best_geometry_last_it_tf FROM jobs WHERE jobs.geom_it_id = '"+str(geom_iteration)+"' GROUP BY jobs.geom_part_id")
        result_set = cursor.fetchall()
        for key in result_set:
            geometry_last_tf_per_particle.append(key['best_geometry_last_it_tf'])

        cursor.execute("SELECT * FROM jobs WHERE geom_it_id = '"+str(geom_iteration)+"' ORDER BY zielfunktion ASC LIMIT 0,1")
        result_set = cursor.fetchall()
        geom_it_id = result_set[0]['geom_it_id']
        geom_part_id  = result_set[0]['geom_part_id']
        volt_it_id  = result_set[0]['volt_it_id']
        part_volt_id  = result_set[0]['part_volt_id']
        cursor.execute("SELECT voltage FROM voltages WHERE geom_iteration_id = '"+str(geom_it_id)+"' AND geom_particle_id = '"+str(geom_part_id)+"' AND voltage_iteration_id = '"+str(volt_it_id)+"' AND voltage_particle_id = '"+str(part_volt_id)+"'")

        result_set = cursor.fetchall()
        best_point = []
        for key in result_set:
            best_point.append(key['voltage'])
        ###################################################################################
        #Rueckgabe wenn eine Geometrieiteration fertig ist
        return best_point,geometry_best_tf_per_particle,geometry_last_tf_per_particle
        #ACHTUNG BEST_POINT IST NOCH NICHT DEFINIERT!!!!!

        #1. bestes X der letzten geometrie iteration
        #3. list mit den besten zielfunktionen fuer jedes geom particle, nach geom particle id sortiert, beginnend bei der kleinsten
        #4. list mit den zielfunktionen der letzten geometrie iteration fuer jedes geom particle, beginnend beim ersten geom particle
        #5. bester Spannungssatz pro Geometrie Particle
        ###################################################################################
    else:
        return False
########################################################################
########################################################################

def get_target_functions_from_db(number_of_particles):

    db = mysql_connect()
    cursor = db.cursor(cursors.DictCursor)

    #wenn ein R stehenbleibt wird der optimizer blockiert
    #hier werden jobs die seit mehr als einer stunde am rechnen sind
    #wieder freigegeben, so dass ein anderer R diese uebernehmen kann
    cursor.execute("UPDATE jobs SET status = '0', id_R = '' WHERE TIME_TO_SEC(datetime) < TIME_TO_SEC(CURTIME())-3600 AND status = '1'");

    cursor.execute("select MAX(job_id) from jobs")
    db_data = cursor.fetchall()
    max_job_id = int( db_data[0]["MAX(job_id)"] )

    #print max_job_id

    cursor.execute("select * from jobs WHERE status = 2 AND job_id > %i ORDER BY job_id DESC" % (max_job_id-number_of_particles) )
    db_data = cursor.fetchall()
    #print db_data
    #raw_input()
    '''
    # finde aktuelle iteration
    cursor.execute("select volt_it_id from jobs ORDER BY job_id DESC LIMIT 0,1")
    db_data = cursor.fetchall()
    this_iteration = int(db_data[0]['volt_it_id'])
    print 'current_iteration = %i' %current_iteration


    cursor.execute("select MAX(volt_it_id) from jobs")
    db_data = cursor.fetchall()
    print db_data[0]
    current_iteration = int(db_data[0]['MAX(volt_it_id)'])
    print 'current_iteration = %i' %current_iteration

    cursor.execute("select * from jobs WHERE status = 2 AND volt_it_id = %i ORDER BY job_id DESC LIMIT 0,%i" % (current_iteration,number_of_particles))
    db_data = cursor.fetchall()
    '''

    target_function = []
    for d in db_data:
        try:
            tf = float(d['zielfunktion'])

            target_function.append(tf)
        except:
            pass

    return target_function


def get_zielf_w_ready_volt():
    datenbank = mysql_connect()
    cursor = datenbank.cursor (cursors.DictCursor)
    print 1
    #wenn ein R stehenbleibt wird der optimizer blockiert
    #hier werden jobs die seit mehr als einer stunde am rechnen sind
    #wieder freigegeben, so dass ein anderer R diese uebernehmen kann
    cursor.execute("UPDATE jobs SET status = '0', id_R = '' WHERE TIME_TO_SEC(datetime) < TIME_TO_SEC(CURTIME())-3600 AND status = '1'");

    print 2
    geom_particles_pronto,geom_iteration,bad_news_list,bad_news_exp_list = get_zielf_w_ready_g(1) #diese Teilchen werden hier ja nicht zurueck gegeben
    string_arr_4_query = "("
    for key in geom_particles_pronto:
        string_arr_4_query += str(key) + ","
        cursor.execute("UPDATE status_of_gem_particle SET status = '1' WHERE geom_it_id = '"+str(geom_iteration)+"' AND geom_part_id = '"+str(key)+"'");
    string_arr_4_query = string_arr_4_query[:-1]
    string_arr_4_query += ")"
    bedingung = ""
    print 3
    if(len(geom_particles_pronto) > 0):
        bedingung =  "AND geom_part_id NOT IN "+string_arr_4_query
    print 4
    #print 'Bedingung'
    #print bedingung
    #print 'Ende Bedingung'
    #time.sleep(2)

    cursor.execute("SELECT MAX(volt_it_id) AS vid, geom_part_id FROM jobs WHERE geom_it_id = '"+str(geom_iteration)+"' "+str(bedingung)+" GROUP BY geom_part_id")

    result_set = cursor.fetchall()
    continue_search = True
    for key in result_set:
        #print 'in schleife sein'
        #time.sleep(2)
        if continue_search:
            #print 'contiuniert suche'
            #time.sleep(2)
            geom_part_id_tmp = key['geom_part_id']
            volt_iter_id = key['vid']

            cursor.execute("SELECT * FROM jobs WHERE geom_it_id = '"+str(geom_iteration)+"' AND geom_part_id = '"+str(geom_part_id_tmp)+"' AND volt_it_id = '"+str(volt_iter_id)+"' AND status != '2'")
            #print "SELECT * FROM jobs WHERE geom_it_id = '"+str(geom_iteration)+"' AND geom_part_id = '"+str(geom_part_id_tmp)+"' AND volt_it_id = '"+str(volt_iter_id)+"' AND status != '2'"
            #time.sleep(8)
            rows = cursor.rowcount
            if rows == 0: #schauen ob alle fertig sind, wenn einer nicht status 2 hat ist er nicht fertig
                print 'Der findet normale fertige'
                #print 'geom part id'
                #print geom_part_id_tmp
                #print 'volt it id'
                #print volt_iter_id
                #time.sleep(2)

                continue_search = False #der hat eine rueckgabe, muss also nicht weitersuchen
                cursor.execute ("SELECT zielfunktion FROM jobs WHERE geom_it_id = '"+str(geom_iteration)+"' AND geom_part_id = '"+str(geom_part_id_tmp)+"' AND volt_it_id = '"+str(volt_iter_id)+"' ORDER BY part_volt_id ASC")
                result_tfs = cursor.fetchall()
                zielffunk_list = []
                for key in result_tfs:
                    zielffunk_list.append(key['zielfunktion'])


    if continue_search: #hat nichts gefunden
        datenbank.close ()
        return False
    else:
        cursor.execute("SELECT voltage_particle_id FROM voltages WHERE geom_iteration_id = '"+str(geom_iteration)+"' AND geom_particle_id = '"+str(geom_part_id_tmp)+"' AND voltage_iteration_id = '"+str(volt_iter_id)+"'")
        result_set = cursor.fetchall()
        iteration_id = volt_iter_id
        X = []
        V = []
        particles_geholt = []
        for key in result_set:
            particle_id = key['voltage_particle_id']
            if particle_id not in particles_geholt:

                cursor.execute ("SELECT voltage,v FROM voltages WHERE geom_iteration_id = '"+str(geom_iteration)+"' AND geom_particle_id = '"+str(geom_part_id_tmp)+"' AND voltage_iteration_id = '"+str(iteration_id)+"' AND voltage_particle_id = '"+str(particle_id)+"' ORDER BY volt_id");
                voltages_set_tmp = cursor.fetchall()
                anz_rows_volt = cursor.rowcount
                voltages_rueckgabe_tmp = []
                v_rueckgabe_tmp = []
                for key_volt in voltages_set_tmp:
                    voltages_rueckgabe_tmp.append(key_volt['voltage'])
                    v_rueckgabe_tmp.append(key_volt['v'])

                X.append(voltages_rueckgabe_tmp)
                V.append(v_rueckgabe_tmp)
                particles_geholt.append(particle_id)


        cursor.execute("SELECT MIN(zielfunktion) AS tf, part_volt_id FROM jobs WHERE geom_it_id = '"+str(geom_iteration)+"' AND geom_part_id = '"+str(geom_part_id_tmp)+"' GROUP BY part_volt_id")
        res_set = cursor.fetchall()
        X_top = []
        zielfunk_best = []
        for key in res_set:
            zielfunk_best.append(key['tf'])
            cursor.execute("SELECT volt_it_id FROM jobs WHERE geom_it_id = '"+str(geom_iteration)+"' AND geom_part_id = '"+str(geom_part_id_tmp)+"' AND part_volt_id = '"+str(key['part_volt_id'])+"' AND zielfunktion = "+str(key['tf'])+" ORDER BY volt_it_id DESC")
            res_volt_it = cursor.fetchall()
            tmp = res_volt_it[0]['volt_it_id']
            cursor.execute("SELECT voltage FROM voltages WHERE  geom_iteration_id = '"+str(geom_iteration)+"' AND geom_particle_id = '"+str(geom_part_id_tmp)+"' AND voltage_particle_id = '"+str(key['part_volt_id'])+"' AND voltage_iteration_id = '"+str(tmp)+"' ORDER BY volt_id ASC")
            res_x_top = cursor.fetchall()
            col_x_top = []
            for volt_x_top in res_x_top:
                col_x_top.append(volt_x_top['voltage'])
            X_top.append(col_x_top)

        datenbank.close ()
        return geom_part_id_tmp,X,X_top,V,zielffunk_list,zielfunk_best,bad_news_list[geom_part_id_tmp],bad_news_exp_list[geom_part_id_tmp]

#   geometrie teilchen id
#   X geometrie teilchen aktuell iteration
#   X TOP von geometrie teilchen matrize fuer jedes einzelne teilchen der beste array (voltages)
#   V geometrie teilchen aktuell iteration
#   tf list von gemetrie teilchen aktuell iteration
#   tf best list von geometrie teilchen vektor der besten tf fuer jedes teilchen, also aus verschiedenen iterationen
#   bad_news vom geometrie teilchen
#   bad_news_exp von geometrie teilchen

########################################################################
########################################################################
