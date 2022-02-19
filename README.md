# gandlf_experiments_template

This repo contains a mechanism to run multiple [GaNDLF](https://github.com/CBICA/GaNDLF) experiments on the UPenn CUBIC cluster.

# Configurations

All configuration options can be changed depending on the experiment at hand. These are just some examples for illustration.
## Common

These options are common for all and do not change. For example, the following are always set for this template:

- Loss function: dc_log
- Weighted loss: True
- Augmentation configurations:
  - higher prob: affine, noise, Bias
  - lower prob: blur, rotations, flip, anisotropic

## Top-level configurations

These are defined by the top-level folders.

| Folder | Optimizer | Patch_Size |
|:------:|:---------:|:----------:|
|    A   |    adam   |   128**3   |
|    B   |    sgd    |   128**3   |
|    C   |    adam   |    64**3   |
|    D   |    sgd    |    64**3   |

## Lower-level configurations

These are defined by the lower-level numerical configs.

| Config |     Scheduler     | Learning Rate |
|:------:|:-----------------:|:-------------:|
|    0   | triangle_modified |      0.1      |
|    1   |  cosineannealing  |      0.1      |
|    2   | triangle_modified |      0.5      |
|    3   |  cosineannealing  |      0.5      |
|    4   | triangle_modified |      1.0      |
|    5   |  cosineannealing  |      1.0      |


# Usage

```bash
python submitter.py -h
usage: GANDLF_Experiment_Submitter [-h] [-i] [-g] [-d] [-r]

Submit GaNDLF experiments on CUBIC Cluster.

Contact: software@cbica.upenn.edu

This program is NOT FDA/CE approved and NOT intended for clinical use.
Copyright (c) 2022 University of Pennsylvania. All rights reserved.

optional arguments:
  -h, --help            show this help message and exit
  -i , --interpreter    Python interpreter to be called.
  -g , --gandlfrun      'gandlf_run' script to be called.
  -d , --datafile       'data.csv' script to be called.
  -r , --runnerscript   'runner.sh' script to be called.
```

- All parameters have _some_ defaults, and should be changed based on the experiment at hand.
- Use this repo as template to create a new **PRIVATE** repo.
- Update email address in `runner.sh` for notifications.
- Update common config properties as needed.
- Edit the `data.csv` file to fill in updated data list (channel list should not matter as long as it is consistent). Ensure you have read access to the data.
- Run `python ./submitter.py` to submit the experiments.