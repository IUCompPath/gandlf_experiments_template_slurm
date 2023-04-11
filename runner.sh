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

if [ $CUDA_VISIBLE_DEVICES != 0 ] ; then
    # Exit with status 99, which tells the scheduler to resubmit the job
    # https://cbica-portal.uphs.upenn.edu/rt/Ticket/Display.html?id=6194 
    exit 99
fi

$1 ../tackle_scratch_space.py -g $2 -d $3 -c $4 -o $5 -f $6

# ## run actual trainer
# $1 $2 \
# --inputdata $3 \
# --config $4 \
# --modeldir $5 \
# --train True \
# --device cuda \
# --reset True # this removes previously saved checkpoints and data
