#!usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
from pathlib import Path

cwd = Path(__file__).resolve().parent
all_files_and_folders = os.listdir(cwd)
runner_file = os.path.join(cwd, 'runner.sh')
data_file = os.path.join(cwd, 'data.csv')
python_interpreter = "/cbica/comp_space/patis/testing/gandlf_mine/venv11/bin/python"
gandlf_run = "/cbica/home/patis/comp_space/testing/gandlf_mine/gandlf_run"

for file_or_folder in all_files_and_folders:
    current_file_or_folder = os.path.join(cwd, file_or_folder)
    if os.path.isdir(current_file_or_folder):
        os.chdir(current_file_or_folder) # change cwd so that logs are generated in single place
        files_and_folders_inside = os.listdir(current_file_or_folder)
        for internal_file_or_folder in files_and_folders_inside:
            # only loop over configs
            if internal_file_or_folder.endswith(".yaml") or internal_file_or_folder.endswith(".yml"):
                current_config = os.path.join(current_file_or_folder, internal_file_or_folder)
                config, _ = os.path.splitext(internal_file_or_folder)
                output_dir = os.path.join(current_file_or_folder, config)
                # delete previous results and logs
                if os.path.isdir(output_dir):
                    shutil.rmtree(output_dir)
                Path(output_dir).mkdir(parents=True, exist_ok=True)

                command = "qsub -N L_" + file_or_folder + "_" + config + " " + runner_file + " " + python_interpreter + " " + gandlf_run + " " + data_file + " " + current_config + " " + output_dir
                print(command)

                # os.system("qsub -N L_" + file_or_folder + "_" + config + " " + runner_file + " " + python_interpreter + " " + gandlf_run + " " + data_file + " " + current_config + " " + output_dir)