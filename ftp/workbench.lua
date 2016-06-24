--this lua file has been modified by simion optimizer
simion.workbench_program()
function segment.init_p_values() 
	simion.early_access() 
	pa1 = simion.wb.instances[1].pa
	pa2 = simion.wb.instances[2].pa
	pa1:fast_adjust {[1] = _G.V1, [2] = _G.V2, [3] = _G.V3}
	pa1:fast_adjust {[4] = 666.0, [5] = 777.0}
end

function segment.other_actions()
	if ion_time_of_flight > 20
	then
		ion_splat = -1
	end
end
