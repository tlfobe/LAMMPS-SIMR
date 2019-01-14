# init.py
import signac
import pyaml

project = signac.init_project('LAMMPS-SIMR')

for t in range(200,1201,200):
   for p in range(1,11,2):
      for poly in ['alpha','beta']:
         param = {'poly': poly, 'p': p, 'T': t}
         job = project.open_job(param)
         job.init()
