# PiRack

This project deals with a solution to face the problem of managing a cluster of Raspberry Pis. A solution named PiRack, using 49 Raspberry Pis and a Master/Slave architecture has been developed. The PiRack set up, its architecture and the management tools developed are presented successively below (for further understanding of the project itself, you should refer to the report provided on the git repository).

The code of the project is divided in 3 parts : client, server and slaves. 

The client files implement a website to control the Pirack remotely and easily (Pirack/master/client). 
The server files implement the Web Server and the Control Server installed on the Master raspberry pi (Pirack/master/server) :
it communicates with the client (Website)
it controls the 48 other slaves (raspberry pis)

The slave files implement the behaviour of the slave raspberry pis regarding the request coming from the master (the slaves are in a listening mode, waiting for a request from the Master).

The installation of the right OS and dependencies on the Master and Slave Raspberry Pis is explained on the piRack-InstallationOfRasbian.pdf file. Once you have gone through these instructions, you have to add some dependencies :

Master dependencies to install:
pip3 : https://pip.pypa.io/en/stable/installing/
pip3 install subprocess
pip3 install sh
pip3 install csv
pip3 install tornado
python3
pip3 install nginx

For now, this code has only been tested using 2 Raspberry Pis and 1 master Raspberry Pi  with the following configuration: 2 raspberry pis gathered in a stack controlled by the master.

Fetch the code from the repository on your computer.

The Web Client files are not currently installed on the Master Raspberry (see the TODO List), so to launch the Web Client, you must do it on your own machine (not connect on the master Raspberry using ssh)
To launch the client Web, you must install node js using the command npm install.

Go to the following directory (you have fetched the client files of the git repository on your own computer) : 
Pirack/master/client
type the following command :
npm start
When it is done, you should have the following message :
Starting up http-server, serving ./ on port: 8000
Hit CTRL-C to stop the server

To connect to the master, use the following SSH command:
ssh pi@192.168.23.11 (master ip address set directly on the cmdline.txt file in the SD card).
The password is “raspberry”.
Copy in the master the directory Pirack/master/server

The first thing to do is to visualize geographically the structure you want for the pirack and to fill the structure_rack.ini (Pirack/master/server) file. This file sets the structure of your Pirack and the IDs distributed to the Stacks.

To start the Server:
Go to the following directory : Pirack/master/server
Type the following command: python3 server.py 

Once the server and the client are started, go to your browser and connect to the website with the following URL : http://localhost:8000/app/

Now that you have login you are redirected to the manage page, go to the install page 
Make sure all the stacks are powered off
Click on the button “launch installation”
The relay module is disabled at first. All stacks are powering down (simulation)
The first switch of the relay module is on (1 stack is powering on). You need to plug manually your first stack
Follow the LED relay module: if a relay power on/off, manually power on/off the corresponding stack.
At the end of the installation, all stacks must be plugged and Raspberry Pis must have asked for their fixed IP addresses to the DHCP server.
Once the installation is completed the progress bar should disappear and the stack should appear on the list with a green Status.

You must then connect to each slave using the command 
ssh root@ip_slave 
and then run the command
slave
You should have the following message :
socket: Success
bind: Success
Ready to receive..

 Afterwards, you can go to the manage page to make actions on the raspberry Pis or on the Stacks.

TODO List :
- put the web client files on the master pi using nginx
- create a service to start the slave at booting of the Pi slave
- the reboot request is not working (clicking on the reboot button from the website provokes a segmentation fault in the slaves)
- the cpu request in not working : the bash script that is executed by the slaves when clicking the button “cpu” on the website requires the use of the “bc” command which must be installed on the Raspberry pis (not installed due to internet issues) (sudo apt-get install bc).
- It is possible to make actions on the raspberry pis, on the stacks but not on the Pirack yet.
- If a new Rasp with empty OS is installed, it is required to send through a script the id_rsa.pub of the master (public key) to the /root/.ssh/authorized_keys file of the slave.

