#!/bin/bash

set -e

# link to LAMMPS
lmp=/home/simon/Softwares/LAMMPS-GUI-1.6.3/lmp

# Choose the chemical potential
for mu in  4600 4400 4200 4000 3800 3600 3400 3200 3000
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
    cd ../topology/lammps
        newline='variable box0 equal '${box0}
        oldline=$(cat input.lmp| grep 'variable box0 equal ')  
        sed -i '/'"$oldline"'/c\'"$newline" input.lmp
        ${lmp} -in input.lmp
    cd ../../lammps-comparison/

    cp ../topology/lammps/H2O-0.data .

    # Replace the chemical potential value in the input
    newline='variable mu_K equal -'${mu}
    oldline=$(cat input.lmp| grep 'variable mu_K equal')
    sed -i '/'"$oldline"'/c\'"$newline" input.lmp

    OMP_NUM_THREADS=8 ${lmp} -in input.lmp -sf omp

    mv *.dat ${data_folder}
    mv log.lammps ${data_folder}

done
