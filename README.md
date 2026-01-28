# machine_coding_round

This repository agregates the files required to run the mini-server.
Assuming it is run on a linux system, it requires python, curl, pip (to install the python libraries), make (to simplify the installation and execution) and the ability to create a virtual environment.
The relevant commands are stored in the makefile.
The adress of the generated server is indicated in the terminal when running "make launch". Usually <search-service-host> = 127.0.0.0.0/5000; but this must be chekced.
The server is queried by calling :

curl http://<search-service-host>/search?q=”string”.
