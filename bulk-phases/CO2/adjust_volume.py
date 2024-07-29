import MDAnalysis as mda

topology_file_0 = "./topology/lammps/CO2-0.data"
topology_file_1 = "./topology/lammps/CO2-1.data"

u_0 = mda.Universe(topology_file_0)
u_1 = mda.Universe(topology_file_1)

box_size_0 = u_0.dimensions[:3]
box_size_1 = u_1.dimensions[:3]

current_input = open("input.gomc", "r")
all_lines = []
for line in current_input:
    if "CellBasisVector1 0" in line:
        line = "CellBasisVector1 0 "+str(box_size_0[0])+" 0.00 0.00\n"
    if "CellBasisVector2 0" in line:
        line = "CellBasisVector2 0 0.00 "+str(box_size_0[1])+" 0.00\n"
    if "CellBasisVector3 0" in line:
        line = "CellBasisVector3 0 0.00 0.00 "+str(box_size_0[2])+"\n"
    if "CellBasisVector1 1" in line:
        line = "CellBasisVector1 1 "+str(box_size_1[0])+" 0.00 0.00\n"
    if "CellBasisVector2 1" in line:
        line = "CellBasisVector2 1 0.00 "+str(box_size_1[1])+" 0.00\n"
    if "CellBasisVector3 1" in line:
        line = "CellBasisVector3 1 0.00 0.00 "+str(box_size_1[2])+"\n"
    all_lines.append(line)
current_input.close()

new_input = open("input.gomc", "w")
for line in all_lines:
    new_input.write(line)
new_input.close()