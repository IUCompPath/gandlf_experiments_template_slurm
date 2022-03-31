import os, pathlib, yaml


current_working_dir = pathlib.Path(os.getcwd()).as_posix()

## make sure you have a baseline configuration somewhere
base_config = os.path.join(current_working_dir, "config.yaml")

### this example is to generate multiple configs based on schedulers and learning rates
# learning_rates = [0.1, 0.01, 0.001, 0.0001]
# schedulers = ["exponential", "step", "reduce_on_plateau", "cosineannealing"]

# for sched in schedulers:
#     base_output_dir = os.path.join(current_working_dir, sched)
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

# current_config_dir = os.path.join(current_working_dir, "exponential")
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

# output_dir = os.path.join(current_working_dir, "B")

# for batch in batch_sizes:
#     config = os.path.join(output_dir, str(batch) + ".yaml")
#     with open(base_config, "r") as f:
#         config_dict = yaml.safe_load(f)
#     config_dict["batch_size"] = batch
#     with open(config, "w") as f:
#         yaml.dump(config_dict, f)
