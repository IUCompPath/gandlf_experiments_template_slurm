#! /bin/bash
#$ -l h_vmem=100G ## amout RAM being requested
#$ -l gpu
##$ -N JOB_NAME_GOES_HERE
#$ -pe threaded 10 ## change number of CPU threads you want to request here
#$ -cwd
#$ -M user@upenn.edu ## change email
# this file is used to run gpu jobs on the cluster in a proper manner so 
# that the CUDA_VISIBLE_DEVICES environment variable is properly initialized
# ref: https://sbia-wiki.uphs.upenn.edu/wiki/index.php/GPU_Computing#Directing_Jobs_to_a_Specific_GPU_with_the_get_CUDA_VISIBLE_DEVICES_Utility
### $1: absolute path to python interpreter in virtual environment
### $2: absolute path to gandlf_run that needs to be invoked
### $3: yaml configuration
### $4: output_dir (relative to cwd)

#module unload cuda/9.2
module load cuda/10.2

## run actual trainer
$1 $2 -data /cbica/home/patis/comp_space/testing/gandlf_mine_refactor/exp_ventricle/data.csv -config $3 -o $4 -train 1 -device cuda -reset_prv True
