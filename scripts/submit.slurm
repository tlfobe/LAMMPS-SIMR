#!/bin/bash
#SBATCH -t 1-12:00:00
#SBATCH --output=logfile
#SBATCH --nodes=1
#SBATCH --ntasks-per-node 4
#SBATCH --partition RM-shared

# load in modules for this job
# module load LAMMPS/lammps-16Mar18 
# tried all 3 lammps modules on bridges, none seem to work, 
# so I intalled one locally

module load mpi/intel_mpi
export lmp_mpi=/home/tfobe/Programs/lammps-22Aug18/src/lmp_mpi

sleep 1 # possibly to give module to load?

echo "SUBMITTED" > jobstatus.txt

# Run lammps
echo "RUNNING LAMMPS"
mpirun -n 4 $lmp_mpi -var tmp TEMP -var prs PRES -var poly POLY< LAMMPS.in  > LAMMPS.out

echo "FINISHED" > jobstatus.txt
echo "Job Ended at `date`"

