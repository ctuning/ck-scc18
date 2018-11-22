#!/bin/bash -l

#SBATCH --job-name=$<<SBATCH_JOB_NAME>>$
#SBATCH --time=$<<SBATCH_TIME>>$
#SBATCH --nodes=$<<SBATCH_NODES>>$
#SBATCH --ntasks-per-core=$<<SBATCH_NTASKS_PER_CORE>>$
#SBATCH --ntasks-per-node=$<<SBATCH_NTASKS_PER_NODE>>$
#SBATCH --cpus-per-task=$<<SBATCH_CPU_PER_TASK>>$
#SBATCH --partition=$<<SBATCH_PARTITION>>$
#SBATCH --constraint=$<<SBATCH_CONSTRAINT>>$

../$1