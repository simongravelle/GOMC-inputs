#!/bin/bash

set -e

# Choose the chemical potential
for mu in 3000 3200 3400 3600 3800 4000 4200 4400 4600
do

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

done

cp ../../scripts/analysis.py .
python3 analysis.py
rm analysis.py
