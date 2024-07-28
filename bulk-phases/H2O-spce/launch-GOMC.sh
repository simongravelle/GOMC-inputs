#!/bin/bash

set -e

# link to LAMMPS
lmp=/home/simon/Softwares/LAMMPS-GUI-1.6.3/lmp

# Choose the chemical potential
for mu in 3000 3200 3400 3600 3800 4000 4200 4400 4600
do

    if [[ $mu -gt 3300 ]]
    then
        # expected vapor
        box0=200
    else
        # expected liquid
        box0=30
    fi
    echo "Chemical potential = -"${mu}" K --- Box size = "${box0}" A"

    # create folder for data saving
    data_folder='outputs_mu'${mu}
    mkdir -p ${data_folder}

    # Adjust initial box size
    # Call LAMMPS
    cd topology/lammps
        newline='variable box0 equal '${box0}
        oldline=$(cat input.lmp| grep 'variable box0 equal ')  
        sed -i '/'"$oldline"'/c\'"$newline" input.lmp
        ${lmp} -in input.lmp
    cd ../../

    # Replace the chemical potential value in the input
    newline='ChemPot H2O -'${mu}
    oldline=$(cat input.gomc| grep 'ChemPot H2O')
    sed -i '/'"$oldline"'/c\'"$newline" input.gomc

    # Ensure that the volume in the input file is consistent
    # with the initial topology
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
