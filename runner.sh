#!/bin/bash

#SBATCH -J job_name
#SBATCH -p gpu
#SBATCH -A slurm-account-name
#SBATCH -o filename_%j.txt
#SBATCH -e filename_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=username@iu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --time=02:00:00

#Load any modules that your program needs
module load python/gpu/x.x.x ## check this

#Run your program
srun ./my_program my_program_arguments

#! /bin/bash
#$ -l h_vmem=100G ## amout RAM being requested
##$ -l gpu # request the more common P100 nodes
##$ -l A40 # to request the less common A40 nodes
## more details in https://sbia-wiki.uphs.upenn.edu/wiki/index.php/GPU_Computing
#$ -pe threaded 10 ## change number of CPU threads you want to request here
#$ -cwd
#$ -m b 
#$ -m e 
# this file is used to run gpu jobs on the cluster in a proper manner so 
# that the CUDA_VISIBLE_DEVICES environment variable is properly initialized
# ref: https://sbia-wiki.uphs.upenn.edu/wiki/index.php/GPU_Computing#Directing_Jobs_to_a_Specific_GPU_with_the_get_CUDA_VISIBLE_DEVICES_Utility
### $1: absolute path to python interpreter in virtual environment
### $2: absolute path to gandlf_run that needs to be invoked
### $3: absolute path to the data.csv file
### $4: yaml configuration
### $5: output_dir (relative to cwd)
### $6: folder to copy to scratch space

echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

# if [ $CUDA_VISIBLE_DEVICES != 0 ] ; then
#     # Exit with status 99, which tells the scheduler to resubmit the job
#     # https://cbica-portal.uphs.upenn.edu/rt/Ticket/Display.html?id=6194 
#     exit 99
# fi

# $1 ../tackle_scratch_space.py -g $2 -d $3 -c $4 -o $5 -f $6


$1 \  # python int
$2 \  # gandlf_run
--inputdata $3 \  # data.csv
--config $4 \  # yaml config
--modeldir $5 \  # output_dir
--train True --device cuda \  # train on cuda
--reset True # this removes previously saved checkpoints and data
