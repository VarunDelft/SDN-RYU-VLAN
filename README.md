# SDN-RYU-VLAN
Code repository of the OpenFlow based Software Defined Networking application built on the RYU controller. The RYU controller is based on OpenFlow 1.3 and interacts with switches running OpenvSwitch 1.2. For simplicity, it is assumed that the topology and the required VLAN configuration (for each switch) is known priory and therefore no topology discovery is carried out in this application.The RYU application is tested for 3 types of networks:A VLAN-Only linear (2 Switch-4 Host) topology ,A VLAN-only topology containing multiple switches and trunk lines and lastly a hybrid network with VLAN aware and Non-VLAN aware switches. The application has been developed such that it is scalable with higher number of nodes and compatible with any kind of VLAN configuration.


Following files are included in the project folder :-

1) VLAN_8021Q.py : The main RYU Controller Application

2) VLAN Config.txt : File Containing VLAN configuration variables for the 3 types of
   network topologies considered. 

3) Custom Topologies Folder : Containing the custom topology python files for each
   if the above networks. (The files may be copied to /mininet/custom folder)

4) Project Report


##### POINTERS BEFORE RUNNING THE CODE ######

1. There are 3 VLAN Configuration variables (port_vlan, access, trunk) defined in
   the controller application file (Under #GLOBAL VARIABLES).
2. Their values for each of the 3 topologies are defined in VLAN Config.txt (Open 
   with Notepad++ in Windows to view clearly)
3. Before executing the application with a given custom topology, please paste the 
   corresponding variable values in the application file.
