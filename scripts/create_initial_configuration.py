import MDAnalysis as mda
import os, sys, git
import numpy as np

import warnings
warnings.filterwarnings('ignore')

# Detect git path
current_path = os.getcwd()
git_repo = git.Repo(current_path, search_parent_directories=True)
git_path = git_repo.git.rev_parse("--show-toplevel")

# Import converters
sys.path.append(git_path + '/converters')
from lmp_to_gomc import PDB_writer, PSF_writer, add_names,  \
    add_residue, detect_label_map

# Define converter
# LAMMPS type to atom name
type_to_name = detect_label_map()
# Name to resname
file = open("name_to_resname.txt", "r")
type_to_resname = []
for line in file:
    type_to_resname.append(line[:-1].split(" "))
file.close()

folder = "gomc/"

# Create folder if missing
if os.path.exists(folder) is False:
    os.mkdir(folder)

# Import universe
u = mda.Universe("lammps/box.data")
u = add_names(u, type_to_name)
u = add_residue(u, type_to_resname)
# Write PDB
PDB_writer(folder+"box.pdb", u, exchanged_molecule=False)
# Write PSF
PSF_writer(folder+"box.psf", u)

# Import universe
u = mda.Universe("lammps/reservoir.data")
u = add_names(u, type_to_name)
u = add_residue(u, type_to_resname)
# Write PDB
PDB_writer(folder+"reservoir.pdb", u, exchanged_molecule=True)
# Write PSF
PSF_writer(folder+"reservoir.psf", u)