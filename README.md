# TDA Playground<img src='https://github.com/drkostas/tda_examples/blob/master/img/snek.png' align='right' width='180' height='104'>

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/drkostas/tda_playground/master/LICENSE)

## Table of Contents

+ [About](#about)
+ [Getting Started](#getting_started)
    + [Prerequisites](#prerequisites)
+ [Installing, Testing, Building](#installing)
+ [Running locally](#run_locally)
    + [Configuration](#configuration)
    + [Execution Options](#execution_options)
        + [TDA Playground Main](#tda_playground_main)
+ [Todo](#todo)
+ [License](#license)

## About <a name = "about"></a>

A playground for topological data analysis.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites <a name = "prerequisites"></a>

You need to have a machine with Python > 3.6 and any Bash based shell (e.g. zsh) installed.

```ShellSession

$ python3.8 -V
Python 3.8.5

$ echo $SHELL
/usr/bin/zsh

```

## Installing, Testing, Building <a name = "installing"></a>

All the installation steps are being handled by the [Makefile](Makefile):

```ShellSession
$ make install
```

## Running the code locally <a name = "run_locally"></a>

In order to run the code, you will only need to change the yml file if you need to, and either run its file directly or
invoke its console script.

<i>If you don't need to change yml file, skip to [Execution Options](#execution_options).

### Modifying the Configuration <a name = "configuration"></a>

There are already two configured yml files ([confs/default.yml](confs/default.yml), [confs/default_print_only.yml](confs/default_print_only.yml)) with the following
structure:

```yaml
tda:
  - config:
      results_folder: res/rips_full_with_polygons_dgm2
      cutoff_min: 0.45
      cutoff_step: 0.1
      cutoff_lim: 7.1
      show_fig: False
      save_fig: True
      create_gif: False
      points:
        - x: 0.0
          y: 0.0
        - x: 0.0
          y: 1.0
        - x: 1.0
          y: 0.0
        - x: 1.0
          y: 1.0
        - x: 4.0
          y: 4.0
        - x: 4.0
          y: 5.414213562373095
        - x: 5.414213562373095
          y: 4.0
        - x: 5.414213562373095
          y: 5.414213562373095
    type: rips
```

### Execution Options <a name = "execution_options"></a>

First, make sure you are in the correct virtual environment:

```ShellSession
$ conda activate tda_playground

$ which python
/home/drkostas/anaconda3/envs/tda_playground/bin/python

```

#### TDA Playground Main <a name = "tda_playground_main"></a>

Now, in order to run the code you can either call the [main.py](tda_playground/main.py) directly, or invoke the `tda_playground_main`
console script.

```ShellSession
$ python tda_playground/play.py --help
```

## TODO <a name = "todo"></a>

Read the [TODO](TODO.md) to see the current task list.

## License <a name = "license"></a>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


