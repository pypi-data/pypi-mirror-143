# Optimate [![Build](https://img.shields.io/badge/build%20with-python3-success?logo=python)](https://www.python.org/) [![Version](https://img.shields.io/badge/license-MIT-success)](https://opensource.org/licenses/MIT) [![GitHub Release](https://img.shields.io/badge/release-v0.0.1-blue)](https://github.com/m0m0khan/optimate)

Optimate is an automatic parameter optimizer for different material models with the ability to optimize creep and relaxation experiments simultaneously. It utilizes minimization algorithms, such as Nelder-Mead and L-BFGS-B.


## Getting Started

### Prerequisites

Minimum requirement to run Optimate is python v3.8.3 or higher and the following python libraries:

+ numpy (v1.21.5 or higher)
+ scipy (v1.8.0 or higher)
+ pandas (v1.4.1 or higher)
+ matplotlib (v3.5.1 or higher)

### Data Files and Naming Convention

The experimental data must be .dat (tab separated) file(s). For creep and relaxation experiment, the headers of the .dat must be *time*, *strain*, *stress*, & *temperature*. For the initial guess file, the headers of the .par must be *temperature*, *E*, and the all the material model parameters respectively. For example, the files present in the Data/ folder of the master branch can be seen.

For the creep and relaxation data files, a naming convention is set which should be strictly followed to ensure smooth running of the program:
1. For creep experiments, the naming convention is:\
Convention: CreSampleName_Stress_Temperature.dat\
Example   : CreBDY55z2_280_550.dat (For sample BDY55z2 at 280 MPa stress and 550 degree Celsius temperature)

2. For relaxation experiments, the naming convention is:\
Convention: RelSampleName_Strain_Temperature.dat    (Note: Strain/1000 is the actual strain of experiment)\
Example   : RelBDY55re1_2_550.dat (For sample BDY55re1 at 0.002 strain and 550 degree Celsius temperature)

3. For initial guess file, the naming convention is:\
Convention: SamplePfz_initial_guess_material-model.par\
Example   : BDY_initial_guess_nb.par

Material-Model Key: Norton-Bailey 'nb'.

**NOTE: Time is in hours, Stress is in MPa, Strain is unitless, Temperature is in degree Celsius, Weight is unitless and Young's Modulus is in MPa in the data files.**\
**Also: For complete and detailed file and naming convention, please see the user manual.**

### Installation

Install optimate, using pip:
```bash
pip install optimate
```

### Usage

The data (experiment files and the initial guess file) in the format and convention as mentioned in the user manual are to be put together.

For using optimate, just browse to the folder containing the data and run:

```bash
optimate [options]
```

Results will be saved in current working directory in the folder OptimateResults.

**NOTE: It is possible to optimize multiple experiments for the same temperature. Please make a separate data file for every experiment following the naming convention.**

```bash
Example optimate -e CreBDY55z11_250_550.dat CreBDY55z10_205_550.dat -o nm -m nb

            
Arguments:
----------
optional arguments:
      -h, --help            show this help message and exit
      -e EXPERIMENT [EXPERIMENT ...], --experiment EXPERIMENT [EXPERIMENT ...]
                            experiment(s) to be optimized
      -o {nm,bfgs}, --optimizer-method {nm,bfgs}
                            optimizer method for the optimizer
      -m {nb,gf,kora,mgf,tkora,rkora}, --material-model {nb,gf,kora,mgf,tkora,rkora}
                            material model to be optimized
      -w WEIGHT_EXP [WEIGHT_EXP ...], --weight-exp WEIGHT_EXP [WEIGHT_EXP ...]
                            weight w.r.t. experiments (in descending order of stress and/or strain)
      -W WEIGHT_TIME [WEIGHT_TIME ...], --weight-time WEIGHT_TIME [WEIGHT_TIME ...]
                            weight w.r.t. time intervals (for 1-10 hrs : 10-MaxTime hrs)
      -c, --convert-unit    convert time unit from hours to seconds
      -p, --plot            save plot(s)
      -t PLOT_TIME, --plot-time PLOT_TIME
                            maximum time value for plotting
      --pic-format {pdf,png}
                            plot picture format, default 'pdf'
      --opti-mode {strain,rate}
                            mode of comparison between experiment and simulation for the residual function, default 'strain'
      --error {mape,mase}   error definition used in the residual function, default 'mase'
      --error-scale {log,lin}
                            scale of optimization in the residual function, default 'log'
      --timeout TIMEOUT     Maximum allowed time (in seconds) for optimization, default 3600 sec
      --max-iter MAX_ITER   Maximum iterations allowed for optimization, default 10000
      -v, --version         display version information
```

Results will be saved in current working Directory in the OptimateResults folder). The optimized parameters are also generated as a .par (tab separated) file.

## Changelog

Please read [CHANGELOG.md](CHANGELOG.md) for details on the features added and updated during subsequent versions.

## Versioning

I am using [SemVer](https://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/m0m0khan/optimate/tags).

## Author

Optimate is written by [Muhammad Mohsin Khan](https://github.com/m0m0khan) (mohsin.khan1@outlook.com).

## License

Optimate is licensed under MIT License (see the [LICENSE.md](LICENSE.md) file for details).

## Project Status

Optimate is currently under development.
