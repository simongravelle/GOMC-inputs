#!/bin/bash

set -e

# set the box 0 size
box0=36
# choose the number of molecule in the reservoir 1
N0=2000

newline='variable box0 equal '${box0}
oldline=$(cat input.lmp| grep 'variable box0 equal ')  
sed -i '/'"$oldline"'/c\'"$newline" input.lmp

newline='variable N0 equal '${N0}
oldline=$(cat input.lmp| grep 'variable N0 equal ')  
sed -i '/'"$oldline"'/c\'"$newline" input.lmp

LMP=/home/simon/Softwares/LAMMPS-GUI-1.6.3/lmp

OMP_NUM_THREADS=4 ${LMP} -in input.lmp -sf omp
