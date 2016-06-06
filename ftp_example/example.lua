--this lua file has been modified by simion optimizer
simion.workbench_program()

function segment.init_p_values() 
	pa1 = simion.wb.instances[1].pa
	pa1_inst1 = simion.wb.instances[1]
	
	pa_inst1.x = 100
	pa_inst1.el = 10
	
	pa1:fast_adjust {[1] = _G.V1,[2] = _G.V2 }
	pa1:fast_adjust {[3] = 0.0}

end

function segment.other_actions()
	if ion_time_of_flight > 200
	then
		ion_splat = -1
	end
end
