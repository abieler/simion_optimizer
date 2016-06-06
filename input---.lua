--this lua file has been modified by simion optimizer
simion.workbench_program()
function segment.init_p_values() 
    simion.early_access() 
    pa1:fast_adjust {[3] = _G.V1, [4] = _G.V2}
    pa1:fast_adjust {[1] = 0.0, [2] = -70.0}
end

function segment.other_actions()
    if ion_time_of_flight > 20
    then
        ion_splat = -1
    end
end
