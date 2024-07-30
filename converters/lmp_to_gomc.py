import numpy as np

def detect_label_map():
    input_file = open("lammps/input.lmp", "r")
    for line in input_file:
        if "labelmap atom" in line:
            maps = line[:-1].split("labelmap atom ")[1].split(" ")
            type_to_name = [maps[i:i+2] for i in range(0,len(maps),2)]
    return type_to_name

def add_names(u, type_to_name):
    names = []
    for type in u.atoms.types:
        for converter in type_to_name:
            if type == converter[0]:
                names.append(converter[1])
    u.add_TopologyAttr("names", names)
    return u

def add_residue(u, type_to_resname):
    resnames = []
    for res in u.residues:
        this_residue = []
        for atom in res.atoms:
            name = atom.name
            for converter in type_to_resname:
                if name == converter[0]:
                    this_residue.append(converter[1])
        this_residue = np.unique(this_residue)
        assert len(this_residue) == 1, """ERROR, inconsistent number of res"""
        resnames.append(this_residue[0])
    u.add_TopologyAttr("resnames", resnames)
    return u

def PDB_writer(filename, u, exchanged_molecule=True):
    u.atoms.write(filename)
    if exchanged_molecule:
        file = open(filename, "r")
        all_lines = []
        for line in file:
            if line[55:67] == " 1.00  0.00 ":
                line = line.replace(" 1.00  0.00 ", " 0.00  1.00 ")
            all_lines.append(line)
        file.close()
        file = open(filename, "w")
        for line in all_lines:
            file.write(line)
        file.close() 






def PSF_writer(filename, u):
    # https://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node23.html
    # atom ID, segment name, residue ID, residue name, atom name, atom type, charge, mass, and an unused 0.
    atoms = []
    for atom in u.atoms:
        id = atom.id
        resname = atom.resname
        resid = atom.resid
        name = atom.name
        # type = atom.type
        mass = atom.mass
        charge = atom.charge
        atoms.append([id, "X", resid, resname, name, name, charge, mass, 0])
    ncolumns = 9
    rowformat = '{:8} {:5} {:5} {:5} {:5} {:5} {:10} {:10} {:5}'

    fid = open(filename,"w")
    fid.write("PSF\n\n")
    fid.write("0 !NTITLE\n\n")
    fid.write(str(u.atoms.n_atoms)+" !NATOM\n")
    fid.write("\n".join(rowformat.format(*row) for row in atoms))

    if len(u.bonds)  > 0:
        fid.write("\n\n")
        fid.write(str(len(u.bonds))+" !NBOND: bonds \n")
        bonds = []
        for bond in u.bonds:
            id1, id2 = bond.atoms.ids
            bonds.append(id1)
            bonds.append(id2)
        ncolumns = 8 # specify desired number of columns
        rowformat = '{:5} {:5} {:5} {:5} {:5} {:5} {:5} {:5}'
        bonds += [""]*(ncolumns-len(bonds)%ncolumns) # make list multiple of ncolumns
        bonds = [bonds[i:i+ncolumns] for i in range(0,len(bonds),ncolumns)] # reshape in rows
        fid.write("\n".join(rowformat.format(*row) for row in bonds))
    else:
        fid.write("\n\n")
        fid.write("0 !NBOND: bonds  \n")

    if len(u.angles)  > 0:
        fid.write("\n\n")
        fid.write(str(len(u.angles))+" !NTHETA: angles \n")
        angles = []
        for angle in u.angles:
            id1, id2, id3 = angle.atoms.ids
            angles.append(id1)
            angles.append(id2)
            angles.append(id3)
        ncolumns = 8 # specify desired number of columns
        rowformat = '{:5} {:5} {:5} {:5} {:5} {:5} {:5} {:5}'
        angles += [""]*(ncolumns-len(angles)%ncolumns) # make list multiple of ncolumns
        angles = [angles[i:i+ncolumns] for i in range(0,len(angles),ncolumns)] # reshape in rows
        fid.write("\n".join(rowformat.format(*row) for row in angles))
    else:
        fid.write("\n\n")
        fid.write("0 !NTHETA: angles  \n")

    fid.write("\n\n")
    fid.write("0 !NPHI: dihedrals  \n")

    fid.write("\n\n")
    fid.write("0 !NIMPHI: impropers  \n")

    fid.write("\n\n")
    fid.write("0 !NDON: donors \n")

    fid.write("\n\n")
    fid.write("0 !NACC: acceptors \n")

    fid.write("\n\n")
    fid.write("0 !NNB  \n")

    fid.write("\n\n")
    fid.write("0 !NGRP \n")

    fid.close()