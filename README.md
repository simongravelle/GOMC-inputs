# GOMC Optimized Monte Carlo files

This repository contains input files for the [GOMC](https://github.com/GOMC-WSU)
Optimized Monte Carlo code. All the inputs are for Monte Carlo simulations performed
in the Grand Canonical ensemble (GCMC).

## Systems

The systems are either bulk CO2, bulk water, or adsorbed molecules in MFI Zeolite.
The CO2 and MFI scripts were taken from the main repository of GOMC.

![CO2-H2O-MFI](micro-pores/CO2-H2O-MFI/vmd/system.png#gh-light-mode-only)
![CO2-H2O-MFI](micro-pores/CO2-H2O-MFI/vmd/system-dm.png#gh-dark-mode-only)

Figure: CO2 (gray and green) and H2O (white and red) adsorbed in a MFI Zeolite (red and yellow).

# CO2/H2O adsorption in MFI porous material

The CO2 model is a rigid model from
[Harris and Yung, J. Phys. Chem., 99 1995](https://pubs.acs.org/doi/10.1021/j100031a034),
the water model is TIP4P-2005, and the temperature is 300 K. 

![CO2-H2O-MFI](micro-pores/CO2-H2O-MFI/CO2-H2O.png#gh-light-mode-only)
![CO2-H2O-MFI](micro-pores/CO2-H2O-MFI/CO2-H2O-dm.png#gh-dark-mode-only)

# CO2 adsorption in MFI porous material (with LAMMPS comparison)

The CO2 model is a rigid model from
[Harris and Yung, J. Phys. Chem., 99 1995](https://pubs.acs.org/doi/10.1021/j100031a034),
and the temperature is 300 K. 

![CO2-MFI](micro-pores/CO2-MFI/CO2-MFI.png#gh-light-mode-only)
![CO2-MFI](micro-pores/CO2-MFI/CO2-MFI-dm.png#gh-dark-mode-only)

![CO2-MFI](micro-pores/CO2-MFI/CO2-MFI-performance.png#gh-light-mode-only)
![CO2-MFI](micro-pores/CO2-MFI/CO2-MFI-performance-dm.png#gh-dark-mode-only)

# Pure CO2 (with LAMMPS comparison)

The CO2 model is a rigid model from
[Harris and Yung, J. Phys. Chem., 99 1995](https://pubs.acs.org/doi/10.1021/j100031a034),
and the temperature is 300 K.

![CO2](bulk-phases/CO2/CO2.png#gh-light-mode-only)
![CO2](bulk-phases/CO2/CO2-dm.png#gh-dark-mode-only)

## Comparing the performance between LAMMPS and GOMC

Both LAMMPS and GOMC simulations were performed using 8 CPU cores,
in the absence of GPU optimizing. Here the number of GCMC move attempts
(successful or not) per minute are compared.

LAMMPS scripts are also provided here, and results from both LAMMPS
and GOMC are compared on the same graph. If you are new to LAMMPS, please
visit [this website](lammpstutorials.github.io)

![CO2](bulk-phases/CO2/CO2-performance.png#gh-light-mode-only)
![CO2](bulk-phases/CO2/CO2-performance-dm.png#gh-dark-mode-only)

