# gandlf_experiments_template

This repo contains a mechanism to run multiple [GaNDLF](https://github.com/CBICA/GaNDLF) experiments on the UPenn CUBIC cluster.

# Configurations

Weighted loss: True

Optimizer configurations:

- A: adam, 128,128,128
- B: sgd, 128,128,128
- C: adam, 64**3
- D: sgd, 64**3

Augmentation configurations:
- higher prob: affine, noise, Bias
- lower prob: blur, rotations, flip, anisotropic

| Config |  Loss  |     Scheduler     | Learning Rate |
|:------:|:------:|:-----------------:|:-------------:|
|    0   | dc_log | triangle_modified |      0.1      |
|    1   | dc_log |  cosineannealing  |      0.1      |
|    2   | dc_log | triangle_modified |      0.5      |
|    3   | dc_log |  cosineannealing  |      0.5      |
|    4   | dc_log | triangle_modified |      1.0      |
|    5   | dc_log |  cosineannealing  |      1.0      |


# How-to

- Use this repo as template to create a new **PRIVATE** repo.
- Update email address in `runner.sh` for notifications.
- Update common config properties as needed.
- Edit the `data.csv` file to fill in updated data list (channel list should not matter as long as it is consistent). Ensure you have read access to the data.
- Run `sh ./submitter.sh` to submit the experiments.