import MDAnalysis as mda
import os, sys, git
import numpy as np

import warnings
warnings.filterwarnings('ignore')

def detect_label_map():
    input_file = open("lammps/input.lmp", "r")
    for line in input_file:
        if "labelmap atom" in line:
            maps = line.split("labelmap atom ")[1].split(" ")[:-1]
            type_to_name = [maps[i:i+2] for i in range(0,len(maps),2)]
    return type_to_name

def detect_resname(type_to_name):
    if ('C' in np.unique(type_to_name)) & ('O' in np.unique(type_to_name)):
        resname = 'CO2'
    elif ('H' in np.unique(type_to_name)) & ('O' in np.unique(type_to_name)):
        resname = 'H2O'
    return resname

# Detect git path
current_path = os.getcwd()
git_repo = git.Repo(current_path, search_parent_directories=True)
git_path = git_repo.git.rev_parse("--show-toplevel")

# Import converters
sys.path.append(git_path + '/converters')
from lmp_to_gomc import PDB_writer, PSF_writer

# Define converter
type_to_name = detect_label_map()
resname = detect_resname(type_to_name)

folder = "gomc/"

# Create folder if missing
if os.path.exists(folder) is False:
    os.mkdir(folder)

# Import universe
u = mda.Universe("lammps/box.data")
# Write PDB
PDB_writer(folder+"box.pdb", u, type_to_name, resname)
# Write PSF
PSF_writer(folder+"box.psf", u, type_to_name, resname)

# Import universe
u = mda.Universe("lammps/reservoir.data")
# Write PDB
PDB_writer(folder+"reservoir.pdb", u, type_to_name, resname)
# Write PSF
PSF_writer(folder+"reservoir.psf", u, type_to_name, resname)
