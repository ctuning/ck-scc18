#
# Developers:
#   - Grigori Fursin, cTuning foundation / dividiti, 2018
#

import os
import sys
import shutil

# *********************************************************************************
# Pre-process function

def ck_preprocess(i):
    ck=i['ck_kernel']
    del i['ck_kernel']

    rt=i['run_time']
    deps=i['deps']
    pass_to_make = i
    pli = i['misc']

    env=i.get('env',{})
    new_env={} # generate new environment and pass to run scripts

    rr={}

    # First linking dataset files to the current tmp dir
    dataset_path=deps['dataset-seissol']['dict']['env']['CK_ENV_DATASET_SEISSOL']
    cur_path=os.getcwd()

    ck.out('')
    ck.out('Linking dataset files to the tmp directory ...')
    ck.out('')

    fparameter='' # File with dataset parameters

    for f in os.listdir(dataset_path):
        ck.out(' * '+f)

        f1=os.path.join(dataset_path,f)
        f2=os.path.join(cur_path,f)

        if f=='parameters.par':
           fparameter=f2
           # Copy parameter file instead of linking since it can be updated in tmp directory
           shutil.copy2(f1, f2)
        elif not os.path.isfile(f2):
           os.system('ln -s '+f1+' '+f2)

    ck.out('')

    # Read parameters file to check extra dirs
    if fparameter!='':
       r=ck.load_text_file({'text_file':fparameter})
       if r['return']>0: return r
       s=r['string']

       # Replace some vars
       x=env.get('LIMIT_SEISSOL_TIME','')
       if x!='':
          j=s.find('EndTime =')
          if j>0:
             j1=s.find('\n', j)
             if j1>0:
                s=s[:j+9]+' '+str(x)+s[j1:]

                # Record updated parameter file
                r=ck.save_text_file({'text_file':fparameter, 'string':s})
                if r['return']>0: return r

       # Search
       for x in ["OutputFile = '", "checkPointFile = '", "MeshFile = '"]:
           j=s.find(x)
           if j>0:
              j1=s.find("'",j+len(x))
              if j1>j:
                 y=s[j+len(x):j1]

                 j=y.find('/')
                 if j>0:
                    y=y[:j]

                 # If MeshFile, record to new env, otherwise create dirs
                 if x.startswith("Mesh"):
                    ck.out('Detected Mesh File: '+y)

                    new_env['CK_SEISSOL_MESH_FILE']=y
                    new_env['CK_SEISSOL_MESH_FILE_NC']=y+'.nc'
                 else:
                    # Create dirs based on dataset config file
                    if not os.path.isdir(y):
                       ck.out('Creating directory: '+y)
                       os.mkdir(y)

    ck.out('')

    # Generate DGPATH
    maple_path=deps['lib-seissol']['dict']['env']['CK_ENV_LIB_SEISSOL_MAPLE']

    r=ck.save_text_file({'text_file':'DGPATH', 'string':maple_path+'\n'})
    if r['return']>0: return r

    # Check job managers
    jm=env.get('JOB_MANAGER','')
    if jm!='':
       if jm=='slurm':
          # Generating slurm file
          template='../ck_run_slurm_template.sh'
          ff='ck_run_slurm_generated.sh'

          # Load template
          r=ck.load_text_file({'text_file':template})
          if r['return']>0: return 
          s=r['string']

          # Processing vars
          for k in env:
              if k.startswith('SBATCH_'):
                 v=str(env[k])
                 s=s.replace('$<<'+k+'>>$', v)

          # Save generated file
          r=ck.save_text_file({'text_file':ff, 'string':s})
          if r['return']>0: return 
       else:
          return {'return':1, 'error':'env.JOB_MANAGER is not recognized'}

    # Finish
    rr['return']=0
    rr['new_env']=new_env
    return rr

# *********************************************************************************
# Post-process function

def ck_postprocess(i):
    ck=i['ck_kernel']
    rt=i['run_time']
    env=i['env']
    deps=i['deps']

    # Dictionary of last run to save
    d={}

    rr={}
    rr['return']=0

    d['env']=env
    d['deps']=deps

    # Check output file
    output_file=rt['run_cmd_out1']
    if os.path.isfile(output_file):
       r=ck.load_text_file({'text_file':output_file, 'split_to_list':'yes'})
       if r['return']>0: return r

       l=r['lst']

       # Try to find job number
       jm=env.get('JOB_MANAGER','')
       if jm!='':
          if jm=='slurm':

             ck.out("=================================================")
             ck.out("Processing SLURM output ...")

             for x in l:
                 x=x.strip().lower()
                 j=x.find('job ')
                 if j>0:
                    job=x[j+4:].strip()

                    ck.out("")
                    ck.out("SLURM job: "+job)

                    d['job_id']=job

    # Save last run info
    r=ck.save_json_to_file({'json_file':'tmp-last-run.json', 'dict':d, 'sort_keys':'yes'})
    if r['return']>0: return r

    return rr

# Do not add anything here!
