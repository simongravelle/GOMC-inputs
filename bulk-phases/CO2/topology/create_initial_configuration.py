import MDAnalysis as mda
import os, sys, git

import warnings
warnings.filterwarnings('ignore')

# Detect git path
current_path = os.getcwd()
git_repo = git.Repo(current_path, search_parent_directories=True)
git_path = git_repo.git.rev_parse("--show-toplevel")

# Import converters
sys.path.append(git_path + '/converters')
from lmp_to_gomc import PDB_writer, PSF_writer

# Define converter
type_to_name = [["1", "O"], ["2", "H"]]

filename = "H2O"
folder = "gomc/"

# Create folder if missing
if os.path.exists(folder) is False:
    os.mkdir(folder)

for N in ["0", "1"]:
    # Import universe
    u = mda.Universe("lammps/"+filename+"-"+N+".data")
    # Write PDB
    PDB_writer(folder+filename+"-id"+N+".pdb", u, type_to_name)
    # Write PSF
    PSF_writer(folder+filename+"-id"+N+".psf", u, type_to_name)
