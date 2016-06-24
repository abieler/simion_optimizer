This directory contains all the files that are needed on the slave nodes to run the simion optimizer.

- Copy the file slave_starter.py into the mystuff folder of the slave
nodes' simion directory (C:\Program Files\SIMION-8.1\mystuff).

- Copy the 4 other files into the ftp directory on this machine (/wherever/simion_optimizer/ftp/) that can be accessed from the working nodes. These files will then be downloaded from the slave nodes once the slave_starter.py script has been started.

--> Copy them first to the ftp directory and then apply the necessary
changes to them so it fits your specific optimization needs (changes
should only be made to the calculate_target_function.py file)
