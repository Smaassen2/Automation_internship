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

    with open(f"{ptm}_edited.txt", "w") as edited_output:
        edited_output.write(info)
        edited_output.truncate(edited_output.tell()-2)
    edited_output.close()
    return ptm

def find_atom_connections(ptm):
    with open(f"{ptm}.txt", "r") as file:
        for line in file:
            if "ATOM" in line and "ATOM H" not in line:
                single_bonds = []
                double_bonds = []
                atom = line.split()[1]
                #print(atom)


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
                
                replacement = figure_out_atom_type(ptm, connections)
                
                remove_spaces = False
                atom_type_to_be_replaced = line.split()[2]
                if len(atom_type_to_be_replaced) > len(replacement):
                    difference = len(atom_type_to_be_replaced) - len(replacement)
                    final_atom_type = replacement + ' ' * difference
                elif len(atom_type_to_be_replaced) < len(replacement):
                    difference = len(replacement) - len(atom_type_to_be_replaced)
                    final_atom_type = replacement
                    remove_spaces = True
                else:
                    final_atom_type = replacement
                
                if remove_spaces == True:
                    line = line.replace(atom_type_to_be_replaced + difference * " ", final_atom_type)
                else:
                    line = line.replace(atom_type_to_be_replaced, final_atom_type)
                print(line.replace("\n", ""))
                
                with open(f"{ptm}_edited.txt", "r") as file3:
                    data = file3.readlines()
                for line3 in data:
                    if f"ATOM {atom} " in line3:
                        line3_split = line3.split()
                        line3.replace(line3_split[2], replacement)
                with open(f"{ptm}_edited.txt", "w") as file4:
                    file4.writelines(data)
                

                    



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
    str_connections = str(connections)
    #print(f"{str_connections} -- {atom_type_replacement[str_connections]}")
    replacement = atom_type_replacement[str_connections]
    return replacement
                    



ptms = ["ARG"]
for ptm in ptms:
    obtain_seperate_rtf(ptm)
    find_atom_connections(ptm)
    #print(data)
    #write_to_top_heav_lib(data)