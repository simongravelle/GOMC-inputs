# GOMC Optimized Monte Carlo files

This repository contains input files for the [GOMC](https://github.com/GOMC-WSU)
Optimized Monte Carlo code. All the inputs are for Monte Carlo simulations performed
in the Grand Canonical ensemble (GCMC).

## Systems

The systems are either bulk CO2, bulk water, or adsorbed molecules in MFI Zeolite.

![CO2-H2O-MFI](micro-pores/CO2-H2O-MFI/vmd/system.png#gh-light-mode-only)
![CO2-H2O-MFI](micro-pores/CO2-H2O-MFI/vmd/system-dm.png#gh-dark-mode-only)

## Comparison with LAMMPS

For some systems, LAMMPS scripts are also provided, and results from both LAMMPS
and GOMC are compared on the same graph. If you are new to LAMMPS, please
visit [this website](lammpstutorials.github.io).

# Pure CO2

The CO2 model is a rigid model from
[Harris and Yung, J. Phys. Chem., 99 1995](https://pubs.acs.org/doi/10.1021/j100031a034),
and the temperature is 300 K.

![CO2](bulk-phases/CO2/CO2.png#gh-light-mode-only)
![CO2](bulk-phases/CO2/CO2-dm.png#gh-dark-mode-only)
