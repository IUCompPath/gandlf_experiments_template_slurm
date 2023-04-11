import os, yaml, pandas, argparse, ast
from datetime import date
from pathlib import Path

if __name__ == "__main__":

    copyrightMessage = (
        "Contact: software@cbica.upenn.edu\n\n"
        + "This program is NOT FDA/CE approved and NOT intended for clinical use.\nCopyright (c) "
        + str(date.today().year)
        + " University of Pennsylvania. All rights reserved."
    )

    cwd = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        prog="GANDLF_Experiment_Submitter",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Submit GaNDLF experiments on CUBIC Cluster.\n\n"
        + copyrightMessage,
    )

    parser.add_argument(
        "-c",
        "--config",
        metavar="",
        default=True,
        type=ast.literal_eval,
        help="Generate config or not. If false, tries to generate succinct information about training.",
    )
    args = parser.parse_args()

    if args.config:
        ## make sure you have a baseline configuration somewhere
        base_config = os.path.join(cwd, "config.yaml")

    #### update configurations to be trained
    ### this example is to generate multiple configs based on schedulers and learning rates
    # learning_rates = [0.1, 0.01, 0.001, 0.0001]
    # schedulers = ["exponential", "step", "reduce_on_plateau", "cosineannealing"]

    # for sched in schedulers:
    #     base_output_dir = os.path.join(cwd, sched)
    #     pathlib.Path(base_output_dir).mkdir(parents=True, exist_ok=True)

    #     for lr in learning_rates:
    #         with open(base_config, "r") as f:
    #             config = yaml.safe_load(f)
    #         config["learning_rate"] = lr
    #         config["scheduler"] = sched
    #         config["opt"] = "sgd"

    #         with open(os.path.join(base_output_dir, str(lr) + ".yaml"), "w") as f:
    #             yaml.dump(config, f)


    ### this example is to generate multiple configs based on a single scheduler (exponential), learning rate (0.01) and different gammas
    # gamma_vals = [1, 0.01, 0.001, 0.0001]

    # current_config_dir = os.path.join(cwd, "exponential")
    # pathlib.Path(current_config_dir).mkdir(parents=True, exist_ok=True)
    # for gamma in gamma_vals:
    #     config_to_write = os.path.join(current_config_dir, "gamma_" + str(gamma) + ".yaml")

    #     with open(base_config, "r") as f:
    #         config = yaml.safe_load(f)
    #     config["learning_rate"] = 0.01
    #     config["scheduler"] = {}
    #     config["scheduler"]["gamma"] = gamma
    #     config["scheduler"]["type"] = "exponential"

    #     with open(config_to_write, "w") as f:
    #         yaml.dump(config, f)


    ### this example is to generate multiple configs based on different batch sizes
    # batch_sizes = [48, 52, 58]

    # output_dir = os.path.join(cwd, "B")

    # for batch in batch_sizes:
    #     config = os.path.join(output_dir, str(batch) + ".yaml")
    #     with open(base_config, "r") as f:
    #         config_dict = yaml.safe_load(f)
    #     config_dict["batch_size"] = batch
    #     with open(config, "w") as f:
    #         yaml.dump(config_dict, f)
    
    else:
        # get information about best config
        dirs_in_cwd = os.listdir(cwd)
        dirs_in_cwd.sort()
        best_info = {"config": [], "train_epoch": [], "valid_epoch": []}
        ## populate the metrics to be shown - example shown for classification
        metrics_to_populate = ["loss", "balanced_accuracy", "accuracy"]
        for metric in metrics_to_populate:
            for type in ["train", "valid"]:
                best_info[type + "_" + metric] = []

        for dir in dirs_in_cwd:
            current_dir = os.path.join(cwd, dir)
            if os.path.isdir(current_dir):
                print("Current directory: ", current_dir)
                config_outputs_in_dir = os.listdir(current_dir)
                config_outputs_in_dir.sort()
                for config_output in config_outputs_in_dir:
                    current_config_output = os.path.join(current_dir, config_output)
                    if os.path.isdir(current_config_output):
                        print("Current config output: ", current_config_output)
                        file_logs_training = os.path.join(current_config_output, "logs_training.csv")
                        file_logs_validation = os.path.join(current_config_output, "logs_validation.csv")
                        if os.path.isfile(file_logs_training) and os.path.isfile(file_logs_validation):
                            with open(file_logs_training, 'r') as fp:
                                len_logs_training = len(fp.readlines())
                            with open(file_logs_validation, 'r') as fp:
                                len_logs_validation = len(fp.readlines())
                            # ensure something other than the log headers have been written
                            if len_logs_training > 2 and len_logs_validation > 2:
                                # sort by loss
                                best_train_loss_row = pandas.read_csv(file_logs_training).sort_values(by="train_loss", ascending=True).iloc[0]
                                best_valid_loss_row = pandas.read_csv(file_logs_validation).sort_values(by="valid_loss", ascending=True).iloc[0]
                                best_info["config"].append(dir + "_" + config_output)
                                best_info["train_epoch"].append(best_train_loss_row["epoch_no"])
                                best_info["valid_epoch"].append(best_valid_loss_row["epoch_no"])
                                for type in ["train", "valid"]:
                                    for metric in metrics_to_populate:
                                        if type == "train":
                                            best_info["{}_{}".format(type, metric)].append(best_train_loss_row["{}_{}".format(type, metric)])
                                        else:
                                            best_info["{}_{}".format(type, metric)].append(best_valid_loss_row["{}_{}".format(type, metric)])

        pandas.DataFrame.from_dict(best_info).to_csv(os.path.join(cwd, "best_info.csv"), index=False)
