# SIMR-LAMMPS

This repo contains an implementation of succesive interpolation of multistate reweighting (SIMR) using LAMMPS MD simulation package. 


We primarily use signac, a python package, to streamline the naming and naviagation of the dataspace.

Scripts include:

1. init.py : creates signac workspace with needed files to run LAMMPS simulations

2. project.py : contains several operations which run and analyze each LAMMPS simulation. Using `python project.py status`, one can check on the status of each simulation

3. mapping.py : (WIP) uses signac framework to implement SIMR technique.

This repo is currently set up to simulate Bi2O3 systems. 
