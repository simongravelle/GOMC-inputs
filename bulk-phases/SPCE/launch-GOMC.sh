#!/bin/bash

set -e

# link to LAMMPS
LMP=/home/simon/Softwares/LAMMPS-GUI-1.6.4/lmp
# link to GOMC
GOMC=/home/simon/Softwares/GOMC/bin/GOMC_CPU_GCMC

# Choose the chemical potential
for mu in {3800..5200..100}
do

    Nstep=2500000
    NCoord=100
    Nb0=0
    Nb1=1600
    if [[ $mu -gt 4500 ]]
    then
        # expected vapor
        box0=80
    else
        # expected liquid
        box0=25        
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
        ${LMP} -in input.lmp
    cd ../../

    # Two possibilities: impose the chemical potential directly, or impose the pressure

    # estimate pressure and replace in the input
    python3 pressure_from_chemical_potential.py "$mu"
    # Replace the chemical potential value in the input
    #newline='ChemPot CO2 -'${mu}
    #oldline=$(cat input.gomc| grep 'ChemPot CO2')
    #sed -i '/'"$oldline"'/c\'"$newline" input.gomc

    newline='RunSteps '${Nstep}
    oldline=$(cat input.gomc| grep 'RunSteps')
    sed -i '/'"$oldline"'/c\'"$newline" input.gomc

    newline='CoordinatesFreq true '${NCoord}
    oldline=$(cat input.gomc| grep 'CoordinatesFreq true')
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

    ${GOMC} +p8 input.gomc > log.gomc

    # create folder for data saving
    data_folder='outputs_mu'${mu}
    mkdir -p ${data_folder}

    mv output_* ${data_folder}
    mv *.dat ${data_folder}
    mv log.gomc ${data_folder}

    cp ../../scripts/analysis.py .
    python3 analysis.py
    rm analysis.py

done
