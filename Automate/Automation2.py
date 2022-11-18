def obtain_seperate_rtf(ptm):
    info = ""
    with open("/home/shahielm/toppar/top_all36_prot.rtf", "r") as file:
        part_of_ptm = False
        for line in file:
            if f"RESI {ptm}" in line:
                part_of_ptm = True
                info = line
            elif "RESI" in line or "PRES" in line:
                part_of_ptm = False
            elif part_of_ptm == True:
                info += line
            
    file.close()            
    with open(f"{ptm}.txt", "w") as output:
        output.write(info)
        output.truncate(output.tell()-2)
    output.close()
    return ptm

def find_atom_connections(ptm):
    with open(f"{ptm}.txt", "r") as file:
        for line in file:
            if "ATOM" in line and "ATOM H" not in line:
                single_bonds = []
                double_bonds = []
                atom = line.split()[1]
                print(atom)
                with open(f"{ptm}.txt", "r") as file2:
                    for line2 in file2:
                        if "BOND" in line2:
                            # to remove newline characters causing every odd line to be blank (starting from 0)
                            strip_line2 = line2.strip()
                            split_line2 = strip_line2.split()
                            split_line2.pop(0)
                            for x, y in grouped(split_line2, 2):
                                if not x.startswith("H") and not y.startswith("H"):
                                    if x == atom:
                                        single_bonds.append(y)
                                    if y == atom:
                                        single_bonds.append(x)
                        elif "DOUBLE" in line2:
                            # to remove newline characters causing every odd line to be blank (starting from 0)
                            strip_line2 = line2.strip()
                            split_line2 = strip_line2.split()
                            split_line2.pop(0)
                            #print(split_line2)
                            for x, y in grouped(split_line2, 2):
                                if not x.startswith("H") and not y.startswith("H"):
                                    if x == atom:
                                        if y not in double_bonds:
                                            double_bonds.append(y)
                                    if y == atom:
                                        if x not in double_bonds:
                                            double_bonds.append(x)

                connections = [atom, single_bonds, double_bonds]
                figure_out_atom_type(ptm, connections)
    
def grouped(iterable, n):
    # iterate each two values (two atoms that have a bond)
    return zip(*[iter(iterable)]*n)

def figure_out_atom_type(ptm, connections):
    #check values!
    atom_type_replacement = {
                            "['N', ['CA'], []]" : "NH1",
                            "['CA', ['CB', 'N', 'C'], []]" : "CT1",
                            "['CB', ['CA', 'CG'], []]" : "CT2",
                            "['CG', ['CB', 'CD'], []]" : "CT2",
                            "['CD', ['CG', 'NE'], []]" : "CT2",
                            "['NE', ['CD', 'CZ'], []]" : "NC2",
                            "['CZ', ['NE', 'NH2'], ['NH1']]" : "C",
                            "['NH1', [], ['CZ']]" : "NC2",
                            "['NH2', ['CZ'], []]" : "NC2",
                            "['C', ['CA', '+N'], ['O']]" : "NC2",
                            "['O', [], ['C']]" : "NC2"
                            }
    connections = str(connections)
    print(f"{connections} -- {atom_type_replacement[connections]}")

ptms = ["ARG"]
for ptm in ptms:
    obtain_seperate_rtf(ptm)
    find_atom_connections(ptm)
    #data = figure_out_atom_type(ptm, connections)
    #print(data)
    #write_to_top_heav_lib(data)