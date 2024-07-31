#!/usr/bin/env python
# coding: utf-8

from chemfiles import Trajectory as chem_traj
import numpy as np
import os

def detect_names(trajectory):
    first_frame = trajectory.read_step(0)
    all_names = []
    for atom in first_frame.atoms:
        all_names.append(atom.name)
    unique_name = np.unique(all_names)
    unique_mass = np.zeros(len(unique_name))
    for atom in first_frame.atoms:
        for i, name in enumerate(unique_name):
            if atom.name == name:
                unique_mass[i] = atom.mass
    return unique_name, unique_mass

if os.path.exists("output_BOX_0.pdb"):
    trajectory = chem_traj("output_BOX_0.pdb")
    all_names, all_masses = detect_names(trajectory)
    counters_vs_time = np.zeros((trajectory.nsteps, len(all_names)),
                                dtype=np.int32)
    # loop on the frames
    step_vector = []
    for i in np.arange(0, trajectory.nsteps):
        frame = trajectory.read_step(i)
        Lx, Ly, Lz = frame.cell.lengths
        volume = np.prod([Lx, Ly, Lz])
        step_vector.append(frame.step)
        # loop on the atoms
        counters = np.zeros(len(all_names), dtype=np.int32)
        for atom, position in zip(frame.atoms, frame.positions):
            if np.sqrt(position[0]**2+position[1]**2+position[2]**2) > 0:
                # store the atom number
                for j, name in enumerate(all_names):
                    if atom.name == name:
                        counters[j] += 1
        for j, counter in enumerate(counters):
            counters_vs_time[i, j] = counter
    step_vector = np.array(step_vector)
    # evaluate if the number of atoms did evolve with time
    # if not, don't save it
    all_diffs = np.sum(np.abs(np.diff(counters_vs_time, axis=0)), axis=0)
    for counters, diff, name, mass in zip(counters_vs_time.T, all_diffs, all_names, all_masses):
        if diff > 0:
            file_name = "number_"+name+".dat"
            np.savetxt(file_name, np.vstack([step_vector, counters]).T)
            file_name = "density_"+name+".dat"
            density = counters * mass / volume # g/mol/A3
            density /= 6.022e23 # g/A3
            density *= (1e8)**3 # g/cm3
            np.savetxt(file_name, np.vstack([step_vector, density]).T)