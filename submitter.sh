#! /bin/bash

for d in */;
do
  cd $d
  for f in *.yaml;
  do
    config="$(basename -- $f | cut -d. -f1)" # this is to have unique log files
    # # debugging
    echo "f=$f"
    echo "d=$d" 
    # # delete information from previous run(s) -- optional but 
    mkdir -p $config
    rm -rf $config/*
    rm -rf *.e*
    rm -rf *.o*
    rm -rf *.pe*
    rm -rf *.po*
    qsub -N L_$config ../runner.sh /cbica/home/patis/comp_space/testing/gandlf_mine/venv_10.2/bin/python /cbica/home/patis/comp_space/testing/gandlf_mine_refactor/gandlf_run /cbica/home/patis/comp_space/testing/gandlf_mine_refactor/exp_ventricle/data.csv $f $config
  done
  cd ..
done
