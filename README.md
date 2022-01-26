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


# How-to

- Use this repo as template to create a new **PRIVATE** repo.
- Update email address in `runner.sh` for notifications.
- Update common config properties as needed.
- Edit the `data.csv` file to fill in updated data list (channel list should not matter as long as it is consistent). Ensure you have read access to the data.
- Run `sh ./submitter.sh` to submit the experiments.