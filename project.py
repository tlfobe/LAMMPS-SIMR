from flow import FlowProject 
import os
import shutil
import re
import numpy as np
import json

class SIMR_signac(FlowProject):
    pass


@FlowProject.label
def has_sub_files(job):
   return job.isfile('submit.slurm')

@FlowProject.label
def has_structure_files(job):
   return job.isfile(job.sp.poly+'.lmp')

@FlowProject.label
def has_param_files(job):
    return job.isfile('bi2o3_potentials.prm')

@FlowProject.label
def finished_running(job):
   if job.isfile('LAMMPS.out'):
      with open(job.fn('LAMMPS.out')) as fn:
          a = fn.read().splitlines()[-2]  # Checks last line of LAMMPS.out to see if end of LAMMPS.in file was reached!
      return a == "All Done!"
   else:
      return False


@FlowProject.label
def data_extracted(job):
    return job.isfile('vol_eng.json')
    

@FlowProject.operation
@FlowProject.post(has_sub_files)
def gen_sub_files(job):
   shutil.copy('scripts/LAMMPS.in',job.fn('LAMMPS.in'))
   shutil.copy('scripts/submit.slurm',job.fn('submit.slurm'))
   shutil.copy('parameters/bi2o3_potentials.prm',job.fn('bi2o3_potentials.prm'))  #should be able to specify file name with yaml file
   shutil.copy(os.path.join('structures',job.sp.poly+'.lmp'), job.fn(job.sp.poly+'.lmp'))
   f = open(job.fn("submit.slurm"),"r")
   lines = f.read()
   lines = re.sub(r'TEMP', str(job.sp.T), lines)
   lines = re.sub(r'PRES', str(job.sp.p), lines)
   lines = re.sub(r'POLY', job.sp.poly+'.lmp', lines)
   f.close()
   f = open(job.fn("submit.slurm"),"w")
   f.write(lines)
   f.close()

@FlowProject.operation
@FlowProject.pre(has_sub_files)
@FlowProject.post.isfile("data.json")
def write_job_to_json(job):
      with open(job.fn('data.json'),'w') as jsonfile:
            status = {
                        "pressure": float(job.sp.p),
                        "temperature": float(job.sp.T),
                        "polymorph": str(job.sp.poly),
                      }
            jsonfile.write(json.dumps(status)+"\n")

@FlowProject.operation
@FlowProject.pre(has_sub_files)
@FlowProject.post.isfile("equil.dcd")
@FlowProject.post.isfile("prod.dcd")
@FlowProject.post(lambda job: 'job_status' in job.document)
def submit_job(job):
   os.chdir(job.workspace())
   os.system("sbatch submit.slurm")
   #with open(job.fn('equil.dcd'), 'w') as fn:
   #   fn.write('TESTING')
   #with open(job.fn('LAMMPS.out'), 'w') as fn:
   #   fn.write('TESTING')
   job.document['job_status'] = 'RUNNING' # if np.random.randint(0,10) >= 4 else 'FINISHED'
   with open(job.fn('status.txt'),'w') as fn:
      fn.write(job.document.job_status)
   os.chdir('../..')


@FlowProject.operation
@FlowProject.pre.after(submit_job)
@FlowProject.pre(finished_running)
@FlowProject.post.isfile('vol_eng.json')
def extract_data(job):
   with open(job.fn('LAMMPS.out')) as x: 
      f = x.read()
   data = re.findall(r'(?<=Step TotEng KinEng PotEng Volume Press Pxx Pyy Pzz)[\n\s\-\.\d]*(?=Loop time of)',f)
   prod = [ a.split() for a in data[2].rstrip().split('\n')]
   steps  = [float(line[0]) for line in prod[1:]]
   volume = [float(line[4]) for line in prod[1:]]
   energy = [float(line[1]) for line in prod[1:]]
   with open(job.fn('vol_eng.json'),'w') as jsonfile:
      eng_vol = {
         "steps": steps,
         "volume": volume,
         "energy": energy
         }
      jsonfile.write(json.dumps(eng_vol)+"\n")


# @FlowProject.operation
# def mapping_script():
   
# @FlowProject.operation
# def MBAR_script(job.):

# @FlowProject.operation
# def PSCP_script(job):




if __name__ == '__main__':
      SIMR_signac().main()
   
