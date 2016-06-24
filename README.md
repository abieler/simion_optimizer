# simion_optimizer

Python scripts to be used together with the ion optics software SIMION.
It is meant to provide a GUI interface to voltage and geometry optimization
of SIMION models.

## Installation
You need a master node which runs the optimization algorithm, GUI component and hosts
a MySQL dababase. The master node is recommended to be a Debian/Ubuntu version. (Recommendation because it was actually tested on Ubuntu). Then you can add as many slave nodes as you want, ideally running Windows. These slave nodes need a working TCP/IP connection to the master node (the MySQL database) in order to get the different parameters to run SIMION with.

### Dependencies Master Node

#### Linux (Debian / Ubuntu)
Under Ubuntu all dependencies can be installed by executing the install.sh script in the projects home folder.

#### OSX and Windows
You have to manually install the dependencies:
* proftpd
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


### Dependencies Slave Nodes

### All OS
* python-mysqldb
* python-ftplib
* python-numpy
