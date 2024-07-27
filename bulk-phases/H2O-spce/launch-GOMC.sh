#!/bin/bash

set -e

# Choose the chemical potential
mu=3004
data_folder='outputs_mu'${mu}
mkdir -p ${data_folder}

newline='ChemPot H2O -'${mu}
oldline=$(cat input.gomc| grep 'ChemPot H2O')
sed -i '/'"$oldline"'/c\'"$newline" input.gomc

# Ensure that the volume in the input file is the right one
cp ../../scripts/adjust_volume.py .
python3 adjust_volume.py
rm adjust_volume.py

# Create the GOMC topology from LAMMPS files
cd topology/
cp ../../../scripts/create_initial_configuration.py .
python3 create_initial_configuration.py
rm create_initial_configuration.py
cd ..

GCMC=/home/simon/Softwares/GOMC/bin/GOMC_CPU_GCMC

${GCMC} +p4 input.gomc

mv output_* ${data_folder}
mv *.dat ${data_folder}

