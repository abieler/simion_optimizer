def import_gemfile(gemfile_name, G):
    '''
    opens the simion gemfile and writes a python function
    (create_gemfile) to generate this gemfile. All geometry parameters
    can be handed over to this function by G [g0, g1, ..., gn].
    
    !!!!!
    These parameters have then to be inserted into the create_gemfile 
    function MANUALLY as G[0], G[1] etc.
    See SIMION Optimizer User Manual for more Information.
    !!!!!
    '''
    
    ifile = open(gemfile_name,'r')
    ofile = open('gemfile_creator.py','w')
    
    ofile.write('#file created by simion optimizer\n')
    ofile.write('def create_gemfile(G):\n')
    gemfile_path = os.path.join("..", "ftp", gemfile_name)
    ofile.write("\tfile=open('%s','w')\n" %(gemfile_path))

        
    for line in ifile:
        print line
        ofile.write("\tfile.write('"+ line.replace('\n','').replace('\r','') + "\\n')\n")
        
    ofile.write('\tfile.close()')
    ifile.close()
    ofile.close()


def write_lua_file(adj_electrodes_pa1,adj_electrodes_pa2,adj_electrodes_pa3,fix_electrodes_pa1,fix_electrodes_pa2,fix_electrodes_pa3,fix_voltages_pa1,fix_voltages_pa2,fix_voltages_pa3,iob_filename,PA_filenames,path): 
        
    lua_not_modified = True
    iob_filename = iob_filename.split('.')[0]
    adj_electrodes = [adj_electrodes_pa1,adj_electrodes_pa2,adj_electrodes_pa3]
    fix_electrodes = [fix_electrodes_pa1,fix_electrodes_pa2,fix_electrodes_pa3]
    fix_voltages = [fix_voltages_pa1,fix_voltages_pa2,fix_voltages_pa3]

    loo = 0
    for i in adj_electrodes:
        loo += len(i)
    
    loo_fix = 0
    for i in fix_electrodes:
        loo_fix += len(i)
        
    try:
        fid = open(path+iob_filename + ".lua","r")
        first_line = fid.readline()
        if str(first_line) == '--this lua file has been modified by simion optimizer\n':
            print 'lua file was modified previousely...'
            lua_not_modified = False
        lua_imported = True
        user_code_lua = []
        k = 0
        first_function_found = False
        for line in fid:
            user_code_lua.append(line)
            if line.split(' ').count('function') and first_function_found == False:
                function_index = k
                first_function_found = True
            k += 1
        fid.close()
    except:
        lua_imported = False
        
    if lua_not_modified:
        #fiid = open('C:\\Program Files (x86)\\SIMION 8.0\\mystuff\\'+iob_filename + '.lua','w')
        fiid = open(path+iob_filename + '.lua','w')
        fiid.write('--this lua file has been modified by simion optimizer\n')
        fiid.write('simion.workbench_program()\n')
        if lua_imported:
            for j in user_code_lua[0:function_index]:
                fiid.write(j)
                user_code_lua.remove(j)
            fiid.write('--now inserting optimizer adjustables \n')
            
            #for k in range(loo):
            #   fiid.write('adjustable V'+str(k+1) + '  = 0 \n')
            fiid.write('\n')
            fiid.write('function segment.init_p_values() \n')
            fiid.write('    simion.early_access() \n')
            j = 1
            for filename in PA_filenames:
                fiid.write("    pa" + str(j) + " = simion.wb.instances["+ str(j) +"].pa")
                fiid.write('\n')
                j += 1
            pa_counter = 1
            voltage_counter = 1
            for electrodes in adj_electrodes:
                s = ''
                for electrode in electrodes:
                    s = s + '[' + str(electrode) + '] = _G.V'+str(voltage_counter) + ', '
                    voltage_counter += 1
                s = s[:-2]
                if len(s) > 3:
                    fiid.write('    pa'+str(pa_counter)+':fast_adjust {')
                    fiid.write(s)
                    fiid.write('}\n')
                pa_counter += 1
            #now fastadjust the fix voltages
            pa_counter = 1
            voltage_counter = 1
            for electrodes,voltages in zip(fix_electrodes,fix_voltages):
                s = ''
                for electrode,voltage in zip(electrodes,voltages):
                    s = s + '[' + str(electrode) + '] = ' +str(voltage) + ', '
                    voltage_counter += 1
                s = s[:-2]
                if len(s) > 3:
                    fiid.write('    pa'+str(pa_counter)+':fast_adjust {')
                    fiid.write(s)
                    fiid.write('}\n')
                pa_counter += 1
            fiid.write('end\n')
            
            
            fiid.write('--inserting user defined functions \n')
            for i in user_code_lua:
                fiid.write(i)
            
            fiid.close()
        else:
            #for k in range(loo):
            #   fiid.write('adjustable V'+str(k+1) + '  = 0 \n')
            #fiid.write('\n')
            fiid.write('function segment.init_p_values() \n')
            fiid.write('    simion.early_access() \n')
            j = 1
            for filename in PA_filenames:
                fiid.write("    pa" + str(j) + " = simion.wb.instances["+ str(j) +"].pa")
                fiid.write('\n')
                j += 1
            pa_counter = 1
            voltage_counter = 1
            for electrodes in adj_electrodes:
                s = ''
                for electrode in electrodes:
                    s = s + '[' + str(electrode) + '] = _G.V'+str(voltage_counter) + ', '
                    voltage_counter += 1
                s = s[:-2]
                if len(s) > 3:
                    fiid.write('    pa'+str(pa_counter)+':fast_adjust {')
                    fiid.write(s)
                    fiid.write('}\n')
                pa_counter += 1
            #now fastadjust the fix voltages
            pa_counter = 1
            voltage_counter = 1
            for electrodes,voltages in zip(fix_electrodes,fix_voltages):
                s = ''
                for electrode,voltage in zip(electrodes,voltages):
                    s = s + '[' + str(electrode) + '] = ' +str(voltage) + ', '
                    voltage_counter += 1
                s = s[:-2]
                if len(s) > 3:
                    fiid.write('    pa'+str(pa_counter)+':fast_adjust {')
                    fiid.write(s)
                    fiid.write('}\n')
                pa_counter += 1
            fiid.write('end\n\n')
            fiid.write('function segment.other_actions()\n')
            fiid.write('    if ion_time_of_flight > 20\n')
            fiid.write('    then\n')
            fiid.write('        ion_splat = -1\n')
            fiid.write('    end\n')
            fiid.write('end\n')
            fiid.close()

