Item Catalog Project
=====================================

Setup:

> This project makes use of the same Linux-based virtual machine (VM). Install VirtualBox/Vagrant:

    VirtualBox from https://www.virtualbox.org/wiki/Downloads

    Vagrant from https://www.vagrantup.com/downloads.html

> Download the VM configuration

	Clone the fullstack-nanodegree-vm from https://github.com/udacity/fullstack-nanodegree-vm

> From your terminal, inside the vagrant subdirectory, run the command vagrant up and vagrant ssh to bring up the VM

> Navigate to vagrant folder and run the following script to setup and populate database:

    python database_setup.py
    python populate_database.py

> Register with google Developers console to fetch client_secrets.json and authenticate with google id

> Replace client_id in login.html with new client_id from client_secrets.

> To install the dependencies, run:
    
    pip  install  -r  requirements.txt

Execution:

After the setup is done, run application.py
