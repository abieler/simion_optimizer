# simion_optimizer

Python scripts to be used together with the ion optics software SIMION.
It is meant to provide a GUI interface to voltage and geometry optimization
of SIMION models.

## Installation
You need a master node which runs the optimization algorithm, GUI component and hosts
a MySQL dababase. The master node is recommended to be a Debian/Ubuntu version. (Recommendation because it was actually tested on Ubuntu). Then you can add as many slave nodes as you want, ideally running Windows. These slave nodes need a working TCP/IP connection to the master node (the MySQL database) in order to get the different parameters to run SIMION with.

### Dependencies Master Node
python2.7.x

#### Linux (Debian / Ubuntu)
Under Ubuntu all dependencies can be installed by executing the install.sh script in the projects home folder.

#### OSX and Windows
You have to manually install the dependencies:
* vsftpd
* php5
* mysql-server
* mysql-client
* phpmyadmin
* python-numpy
* python-scipy
* python-mysqldb
* python-ftplib
* python-serial
* python-qt4
* python-qwt5-qt4
* python-matplotlib
* python-tk

On the master node you need to set up an fpt server that enables the users
to connect to the folder simion_optimizer/ftp

Set up phpmyadmin and mysql with a user and password such that you are able
to login from the webbrowser typing 'localhost/phpmyadmin'
Once logged in go to the 'Databases' tab and create a database named simion_optimizer_db.
After creation go to the 'Import' tab and import the file simion_optimizer_db.sql from the
simion_optimizer/input directory.

All the user and password names for the mysql database and the ftp server have to be put
into the slave.config file which is in the R_files directory. Look at the present example
to see the list of necessary entries in slave.config

### Dependencies Slave Nodes
python2.7.x
simion >= 8.1
add simion to your path variable, such that you can start simion from the command line
by typing simion.
SIMION_VER in the slave.config file is the name of the simion executable you want to be
run.

### All OS
* python-mysqldb
* python-ftplib
* python-numpy
