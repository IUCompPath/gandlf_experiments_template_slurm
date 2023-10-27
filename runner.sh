#!/bin/bash

###SBATCH -J job_name
#SBATCH -p gpu
###SBATCH -A slurm-account-name
#SBATCH -o filename_%j.txt
#SBATCH -e filename_%j.err
#SBATCH --mail-type=ALL
###SBATCH --mail-user=username@iu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
###SBATCH --time=02:00:00

#Load any modules that your program needs
module load python/gpu/3.10.10

echo $SLURM_JOB_NODELIST
echo $SLURM_JOB_NUM_NODES
echo $SLURM_TASKS_PER_NODE
echo $SLURM_GPUS

nvidia-smi -L

### print out some useful execute node information
numcpu=`grep -c processor /proc/cpuinfo`
echo "Number of CPUs: $numcpu"
mem_ask=`grep MemTotal /proc/meminfo`
echo $mem_ask

### Are the GPUs there? This tells you what type of GPUs are present
echo "GPUs located:"
lspci | grep NVIDIA
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"


# $1 ../tackle_scratch_space.py -g $2 -d $3 -c $4 -o $5 -f $6


$1 \  # python interpreter
$2 \  # gandlf_run
--inputdata $3 \  # data.csv
--config $4 \  # yaml config
--modeldir $5 \  # output_dir
--train True --device cuda \  # train on cuda
--reset True # this removes previously saved checkpoints and data
