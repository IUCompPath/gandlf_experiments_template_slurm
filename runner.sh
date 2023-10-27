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
module load python/gpu/x.x.x ## check this

echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

# if [ $CUDA_VISIBLE_DEVICES != 0 ] ; then
#     # Exit with status 99, which tells the scheduler to resubmit the job
#     # https://cbica-portal.uphs.upenn.edu/rt/Ticket/Display.html?id=6194 
#     exit 99
# fi

# $1 ../tackle_scratch_space.py -g $2 -d $3 -c $4 -o $5 -f $6


$1 \  # python interpreter
$2 \  # gandlf_run
--inputdata $3 \  # data.csv
--config $4 \  # yaml config
--modeldir $5 \  # output_dir
--train True --device cuda \  # train on cuda
--reset True # this removes previously saved checkpoints and data
