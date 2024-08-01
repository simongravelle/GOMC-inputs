#!/bin/bash

set -e

# link to LAMMPS
LMP=/home/simon/Softwares/LAMMPS-GUI-1.6.4/lmp

# Choose the chemical potential
for mu in {2800..5000..200}
do
    Nstep=2500000
    Nb0=5
    Nattempt=100
    echo "Chemical potential = -"${mu}" K"

    # Adjust initial box size
    # Call LAMMPS
    cd ../topology/lammps
        newline='variable Nb0 equal '${Nb0}
        oldline=$(cat input.lmp| grep 'variable Nb0 equal')  
        sed -i '/'"$oldline"'/c\'"$newline" input.lmp
        ${LMP} -in input.lmp
    cd ../../lammps-comparison/

    cp ../topology/lammps/box.data .
    cp ../topology/lammps/parm.lmp .
    cp ../topology/lammps/CO2.mol .

    # Replace the chemical potential value in the input
    newline='variable mu_K equal -'${mu}
    oldline=$(cat input.lmp| grep 'variable mu_K equal')
    sed -i '/'"$oldline"'/c\'"$newline" input.lmp

    newline='variable Nstep equal '${Nstep}
    oldline=$(cat input.lmp| grep 'variable Nstep equal')
    sed -i '/'"$oldline"'/c\'"$newline" input.lmp

    newline='variable Nattempt equal '${Nattempt}
    oldline=$(cat input.lmp| grep 'variable Nattempt equal')
    sed -i '/'"$oldline"'/c\'"$newline" input.lmp
    
    OMP_NUM_THREADS=8 ${LMP} -in input.lmp -sf omp

    # create folder for data saving
    data_folder='outputs_mu'${mu}
    mkdir -p ${data_folder}

    mv *.dat ${data_folder}
    mv log.lammps ${data_folder}

    rm parm.lmp
    rm box.data
    rm CO2.mol

done
