import numpy as np
import os

# Directory scanner
def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

# Folder detector
def scan_directory(ureg, dir_lammps = False, binary_fluid = False):
    subfolders= fast_scandir("./")
    filtered_subfolders = []
    for dir in subfolders:
        if "outputs_" in dir:
            if dir_lammps:
                if "lammps-comparison" in dir:
                    filtered_subfolders.append(dir)
            else:
                if "lammps" not in dir:
                    filtered_subfolders.append(dir)
    chemical_potentials_K = []
    for dir in filtered_subfolders:
        if binary_fluid:
            mu_K_CO2 = np.float32(dir.split("_")[-2][5:])
            mu_K_H2O = np.float32(dir.split("_")[-1][5:])
            chemical_potentials_K.append([mu_K_CO2, mu_K_H2O])
        else:
            mu_K = np.float32(dir.split("_")[-1][2:])
            chemical_potentials_K.append(mu_K)
    chemical_potentials_K = np.array(chemical_potentials_K)
    chemical_potentials_K = chemical_potentials_K *ureg.degree_Kelvin
    return filtered_subfolders, chemical_potentials_K

def measure_isotherm(dirs, atoms, ureg, data_type = "density"):
    out_data = []
    if len(dirs) != 0:
        for dir in dirs:
            mean_out = 0
            for atom in atoms:
                if data_type == "density":
                    out = np.loadtxt(dir+"/density_"+atom+".dat")[:,1]
                elif data_type == "pressure":
                    out = np.loadtxt(dir+"/density_"+atom+".dat")[:,1]
                N_end = len(out)//50
                mean_out += np.mean(out[-N_end:])
            out_data.append(mean_out)
        out_data = np.array(out_data)
        if data_type == "density":
            out_data *= ureg.gram/ureg.centimeter**3
        elif data_type == "pressure":
            out_data *= ureg.atm
    return out_data

def evaluate_gomc_performances(dirs, mus):
    performance_gomc = []
    for dir, mu in zip(dirs, mus):
        log_file = open(dir+"/log.gomc")
        time_measured = False
        for line in log_file:
            if "MOVE_0" in line:
                _, STEP, DISTRY, DISACCEPT, DISACCEPT_, DISMAX, ROTATE, ROTACCEPT, ROTACCEPT, ROTMAX, REGROWTH, REGROWACCEPT, REGROWACCEPT_, TRANSFER, TRANACCEPT, TRANACCEPT = ' '.join(line.split(" ")).split()
                total_GCMC_attempts = np.int32(TRANSFER)
            if ("Simulation ends in" in line) & (time_measured is False):
                d = ' '.join(line.split(" ")).split()[5]
                h = ' '.join(line.split(" ")).split()[7]
                m = ' '.join(line.split(" ")).split()[9]
                total_time = np.float32(d)*60*24+np.float32(h)*60+np.float32(m) # minutes
                time_measured = True
        performance_gomc.append([mu, total_time, total_GCMC_attempts])
    return np.array(performance_gomc)