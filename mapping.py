#!/usr/bin/python
# Analysis scripts for mapping same phase energies to each other using signac

import signac
import numpy as np
import subprocess
import pdb
import os
import sys
import pandas
import mdtraj as md
import shutil
import yaml


#need to make yaml not just enumerate all ts and ps, but give other info like mapping type, nequil etc

project = signac.get_project()
with open('test.yaml') as fn:
    schema = yaml.load(fn)

nenergies = 3000  # should be read from the files, not hard coded
nequil = 1000 
nevery = 1 
mapping = ['volume','harmonic']  # both harmonic and volume
integration = 'direct'
ensemble = 'NPT'

polys = schema['poly']
T = schema['T']
P = schema['p']
# probably don't need these Tstate Pstates...
Tstates = [ list(map(int, T)) for i in range(len(P))] #make an array of all states T,P
Tstates = np.array(Tstates).flatten() #flatten into np.arrays for use
Pstates = [ list(map(int, str(P[i]).split()*len(T))) for i in range(len(P))] #same thing here
Pstates = np.array(Pstates).flatten()

states = len(Tstates)

Lsizeold = dict()
Lsizenew = dict()
npoints = ()(nenergies-nequil)/nevery+1

for poly in polys:
    u_kln = np.zeros([nstatesoldm nstatesnew, npoints], float)
    print('start running')


# Volume Scaling Loop
    for job in project.find_jobs({'poly':poly}):
        job_data = json.load(job.fn('vol_eng.json'))
        volumes = np.array(job_data['volume'])
        volumes = volumes[nequil:]
        avg_v = np.mean(volumes)
        if 'volume' in mapping:
            Lsizeold[job.workspace()] = avg_v**(1.0/3.0)
            Lsizenew[job.workspace()] = avg_v**(1.0/3.0)
        else:
            Lsizeold[job.workspace()] = 1
            Lsizenew[job.workspace()] = 1
        with open('old_v.txt', 'a') as fn:
            fn.write("%4i %4i %10.4f %10.4f +/- %6.4f\n" % (Lsizeold[job.workspace()], avg_v, np.std(volumes)
        with open('new_v.txt', 'a') as fn:
            fn.write("%4i %4i %10.4f %10.4f +/- %6.4f\n" % (Lsizenew[job.workspace()], avg_v, np.std(volumes)
    

    original_v = np.zeros([states, states], float)
    original_e = np.zeros([states, states], float)
    new_v = np.zeros([states,states, npoints])
    new_e = np.zeros([states,states, npoints])
    lnJcbn = np.zeros([states,states])

    for job1 in project.find_jobs({'poly':poly}):
        for job2 in project.find_jobs({'poly':poly}):
            # need to remove bc for calculation of volume
            os.system('babel '+job1.fn('mini.xyz')+' -opdb > '+job1.fn('mini.pdb')) 
            #mdtraj can't read xyz files, quick convert to pdb
            t = md.load(job1.fn('prod.dcd'), top=job1.fn('mini.pdb'))
            tnojump = t.image_molecules()

            
            print(len(t))
            
            # Extract trajectories as mdtraj.Traj object
            tscale = tnojump.slice(range(tnojump.n_frames), copy=True)
            

            # Conditionals based on type of mapping
            
            #if 'NVT' in dirtext:
            #    NVTvolume = tnojump[0].unitcell_volumes[0]
            
            #if 'harmonic' in mapping:
                temperature_scale = np.sqrt(job1.sp.T/job2.sp.T)
            #else:
            #    temperature_scale = 1
            
            #if 'NPT' in dirtext:
            # for now make it work for just NPT, Harmonic, can adjust later on

            tscale.xyz = np.array([ tscale.xyz[s]*np.matrix(ts.unitcell_vectors)**-1 for s, ts in enumerate(tscale)])

            # Temperature mapping (So MBAR does can converge)
            means = np.mean(tsacle.xyz, axis=0)
            divergences = (tscale.xyz-means)*temperature_scale
            tscale.xyz = divergences+means
            tscale.unitcell_vectors *= Lsizenew[job2.workspace()]/Lsizeold[job1.workspace()]

            #if 'NPT' in dirtext:
            tscale.xyz = np.array([ tscale.xyz[s]*np.matrix(ts.unitcell_vectors) for s, ts in enumerate(tscale)])
            tscale.save(job1.fn('prod_mapped.dcd'))
             
            # Need script reruns trajectories here

