# GaNDLF Experiments Template

This repo contains a mechanism to run multiple [GaNDLF](https://github.com/CBICA/GaNDLF) experiments on the UPenn CUBIC cluster.

## Pre-requisites

- This repo will allow you to submit **multiple** GPU jobs on the cluster, which gives you great power; and you know [what comes with that](https://memegenerator.net/img/instances/10306177/with-great-power-comes-great-responsibility-albus-dumbledore.jpg). If Mark's wrath falls upon you, you are on your own.
- Be intimately familiar with the data you are going to use.
- Be familiar with [GaNDLF's usage](https://cbica.github.io/GaNDLF/usage), and try to do a single epoch training on [the toy dataset](https://cbica.github.io/GaNDLF/usage#examples).
- You have [installed GaNDLF](https://cbica.github.io/GaNDLF/setup) on your home directory or comp_space.
- You have run a single epoch of the GaNDLF training loop (training and validation) using your own data _somewhere_ (either CUBIC cluster or own machine - doesn't matter), so that you know how to [customize the configuration](https://cbica.github.io/GaNDLF/usage#customize-the-training).

## Configurations

All configuration options can be changed depending on the experiment at hand. 

In the file [`config_generator.py`](./config_generator.py)
### Common

These options are common for all and do not change. For example, the following are always set for this template:

- Loss function: dc_log
- Weighted loss: True
- Augmentation configurations:
  - higher prob: affine, noise, Bias
  - lower prob: blur, rotations, flip, anisotropic

### Top-level configurations

These are defined by the top-level folders.

| Folder | Optimizer | Patch_Size |
|:------:|:---------:|:----------:|
|    A   |    adam   |   128**3   |
|    B   |    sgd    |   128**3   |
|    C   |    adam   |    64**3   |
|    D   |    sgd    |    64**3   |

### Lower-level configurations

These are defined by the lower-level numerical configs.

| Config |     Scheduler     | Learning Rate |
|:------:|:-----------------:|:-------------:|
|    0   | triangle_modified |      0.1      |
|    1   |  cosineannealing  |      0.1      |
|    2   | triangle_modified |      0.5      |
|    3   |  cosineannealing  |      0.5      |
|    4   | triangle_modified |      1.0      |
|    5   |  cosineannealing  |      1.0      |


## Usage

```bash
python submitter.py -h
usage: GANDLF_Experiment_Submitter [-h] [-i] [-g] [-d] [-r]

Submit GaNDLF experiments on CUBIC Cluster.

Contact: software@cbica.upenn.edu

This program is NOT FDA/CE approved and NOT intended for clinical use.
Copyright (c) 2022 University of Pennsylvania. All rights reserved.

optional arguments:
  -h, --help            show this help message and exit
  -i , --interpreter    Full path of python interpreter to be called. 
  -g , --gandlfrun      Full path of 'gandlf_run' script to be called.
  -d , --datafile       Full path to 'data.csv'.
  -r , --runnerscript   'runner.sh' script to be called.
  -e , --email          Email address to be used for notifications.
```

- All parameters have _some_ defaults, and should be changed based on the experiment at hand.
- Use this repo as template to create a new **PRIVATE** repo.
- Update common config properties as needed.
- Edit the `data.csv` file to fill in updated data list (channel list should not matter as long as it is consistent). Ensure you have read access to the data.
- Run `python ./submitter.py` with correct options (**OR** change the defaults - whatever is easier) to submit the experiments.