#!usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil, argparse
from datetime import date
from pathlib import Path


# main function
if __name__ == "__main__":
    copyrightMessage = (
        "Contact: software@cbica.upenn.edu\n\n"
        + "This program is NOT FDA/CE approved and NOT intended for clinical use.\nCopyright (c) "
        + str(date.today().year)
        + " University of Pennsylvania. All rights reserved."
    )

    cwd = Path(__file__).resolve().parent
    all_files_and_folders = os.listdir(cwd)

    parser = argparse.ArgumentParser(
        prog="GANDLF_Experiment_Submitter",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Submit GaNDLF experiments on CUBIC Cluster.\n\n"
        + copyrightMessage,
    )

    parser.add_argument(
        "-i",
        "--interpreter",
        metavar="",
        default="/cbica/comp_space/patis/testing/gandlf_mine/venv11/bin/python",
        type=str,
        help="Full path of python interpreter to be called.",
    )
    parser.add_argument(
        "-g",
        "--gandlfrun",
        metavar="",
        default="/cbica/home/patis/comp_space/testing/gandlf_mine/gandlf_run",
        type=str,
        help="Full path of 'gandlf_run' script to be called.",
    )
    parser.add_argument(
        "-d",
        "--datafile",
        metavar="",
        default=os.path.join(cwd, "data.csv"),
        type=str,
        help="Full path to 'data.csv'.",
    )
    parser.add_argument(
        "-f",
        "--foldertocopy",
        metavar="",
        default=None,
        type=str,
        help="Full path to the data folder to copy into the location in '$CBICA_TMP'.",
    )
    parser.add_argument(
        "-r",
        "--runnerscript",
        metavar="",
        default=os.path.join(cwd, "runner.sh"),
        type=str,
        help="'runner.sh' script to be called.",
    )
    parser.add_argument(
        "-e",
        "--email",
        metavar="",
        default="user -at- site.domain",
        type=str,
        help="Email address to be used for notifications.",
    )
    parser.add_argument(
        "-gpu",
        "--gputype",
        metavar="",
        default="gpu",
        type=str,
        help="The parameter to pass after '-l' to the submit command.",
    )
    parser.add_argument(
        "-gpur",
        "--gpuratio",
        metavar="",
        default=4,
        type=int,
        help="The number of jobs (starting from '0') to send to 'gpu' vs 'A40', since 'gpu' is more prevalent - ignores parameter `--gputype`.",
    )

    args = parser.parse_args()

    all_files_and_folders.sort()
    counter = 0  # used to change the gpu type for submission
    jobs_that_have_run, jobs_that_have_not_run = 0, 0
    for file_or_folder in all_files_and_folders:
        current_file_or_folder = os.path.join(cwd, file_or_folder)
        if os.path.isdir(current_file_or_folder):
            if file_or_folder != ".git":
                print("*****Folder:", file_or_folder)
                # change cwd so that logs are generated in single place
                os.chdir(current_file_or_folder)
                files_and_folders_inside = os.listdir(current_file_or_folder)
                files_and_folders_inside.sort()

                for internal_file_or_folder in files_and_folders_inside:
                    # only loop over configs
                    if internal_file_or_folder.endswith(
                        ".yaml"
                    ) or internal_file_or_folder.endswith(".yml"):
                        current_config = os.path.join(
                            current_file_or_folder, internal_file_or_folder
                        )
                        config, _ = os.path.splitext(internal_file_or_folder)
                        output_dir = os.path.join(current_file_or_folder, config)
                        Path(output_dir).mkdir(parents=True, exist_ok=True)
                        need_to_run = True
                        if os.path.isdir(output_dir):
                            files_in_output_dir = os.listdir(output_dir)
                            files_in_output_dir.sort()
                            for output_files in files_in_output_dir:
                                if output_files.endswith("_best.pth.tar"):
                                    need_to_run = False
                                    break
                        # # delete previous results and logs
                        # if os.path.isdir(output_dir):
                        #     shutil.rmtree(output_dir)
                        # Path(output_dir).mkdir(parents=True, exist_ok=True)

                        # this can be used to only submit those experiments that have not generated results
                        # condition = not os.path.isfile(os.path.join(output_dir, "logs_validation.csv")) or not os.path.isfile(os.path.join(output_dir, "logs_training.csv"))

                        # if previous results are absent, delete and re-launch
                        if need_to_run:
                            shutil.rmtree(output_dir)
                            Path(output_dir).mkdir(parents=True, exist_ok=True)

                            ## since A40 is less available than gpu, we will use gpu for 3 out of 4 jobs - change as needed
                            if isinstance(args.gpuratio, int):
                                modified_gpu = "gpu"
                                if counter == args.gpuratio:
                                    modified_gpu = "A40"
                                    counter = -1
                            else:
                                modified_gpu = args.gputype

                            command = (
                                "qsub -N L_"
                                + file_or_folder
                                + "_"
                                + config
                                + " -M "
                                + args.email
                                + " -l "
                                + modified_gpu
                                + " "
                                + args.runnerscript
                                + " "
                                + args.interpreter
                                + " "
                                + args.gandlfrun
                                + " "
                                + args.datafile
                                + " "
                                + current_config
                                + " "
                                + output_dir
                                + " "
                                + str(args.foldertocopy)
                            )
                            print(command)
                            os.system(command)
                            counter += 1
                            jobs_that_have_not_run += 1
                        else:
                            jobs_that_have_run += 1

    print("Jobs that have run:", jobs_that_have_run)
    print("Jobs that have not run:", jobs_that_have_not_run)
