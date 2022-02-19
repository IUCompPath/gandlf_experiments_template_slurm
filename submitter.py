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
        help="Python interpreter to be called.",
    )
    parser.add_argument(
        "-g",
        "--gandlfrun",
        metavar="",
        default="/cbica/home/patis/comp_space/testing/gandlf_mine/gandlf_run",
        type=str,
        help="'gandlf_run' script to be called.",
    )
    parser.add_argument(
        "-d",
        "--datafile",
        metavar="",
        default=os.path.join(cwd, "data.csv"),
        type=str,
        help="'data.csv' script to be called.",
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
        default="USER@UPENN.EDU",
        type=str,
        help="Email address to be used for notifications.",
    )

    args = parser.parse_args()

    print("GaNDLF is ready. See https://cbica.github.io/GaNDLF/usage")

    for file_or_folder in all_files_and_folders:
        current_file_or_folder = os.path.join(cwd, file_or_folder)
        if os.path.isdir(current_file_or_folder):
            print("*****Folder: " + file_or_folder)
            os.chdir(
                current_file_or_folder
            )  # change cwd so that logs are generated in single place
            files_and_folders_inside = os.listdir(current_file_or_folder)
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
                    # delete previous results and logs
                    if os.path.isdir(output_dir):
                        shutil.rmtree(output_dir)
                    Path(output_dir).mkdir(parents=True, exist_ok=True)

                    command = (
                        "qsub -N L_"
                        + file_or_folder
                        + "_"
                        + config
                        + " -M "
                        + args.email
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
                    )
                    print(command)
                    os.system(command)
