#!/bin/bash

set -e

# link to LAMMPS
lmp=/home/simon/Softwares/LAMMPS-GUI-1.6.3/lmp

# Choose the chemical potential
for mu in 4600 5000 5400 5800
do

    Nstep=5000000
    NCoord=100000
    if [[ $mu -gt 3600 ]]
    then
        # expected vapor
        box0=140
	Nb0=3000
        Nb1=200
    else
        # expected liquid
        box0=25
	Nb0=1000
        Nb1=2000
    fi
    echo "Chemical potential = -"${mu}" K --- Box size = "${box0}" A"

    # Adjust initial box size
    # Call LAMMPS
    cd topology/lammps
        newline='variable box0 equal '${box0}
        oldline=$(cat input.lmp| grep 'variable box0 equal ')  
        sed -i '/'"$oldline"'/c\'"$newline" input.lmp
        newline='variable Nb1 equal '${Nb1}
        oldline=$(cat input.lmp| grep 'variable Nb1 equal ')  
        sed -i '/'"$oldline"'/c\'"$newline" input.lmp
        newline='variable Nb0 equal '${Nb0}
        oldline=$(cat input.lmp| grep 'variable Nb0 equal ')
        sed -i '/'"$oldline"'/c\'"$newline" input.lmp
        ${lmp} -in input.lmp
    cd ../../

    newline='RunSteps '${Nstep}
    oldline=$(cat input.gomc| grep 'RunSteps')
    sed -i '/'"$oldline"'/c\'"$newline" input.gomc

    newline='CoordinatesFreq true '${NCoord}
    oldline=$(cat input.gomc| grep 'CoordinatesFreq true')
    sed -i '/'"$oldline"'/c\'"$newline" input.gomc

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

    ${GCMC} +p8 input.gomc

    # create folder for data saving
    data_folder='outputs_mu'${mu}
    mkdir -p ${data_folder}

    mv output_* ${data_folder}
    mv *.dat ${data_folder}

done

cp ../../scripts/analysis.py .
python3 analysis.py
rm analysis.py
