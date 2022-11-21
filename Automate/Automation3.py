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
    all_connections = []
    with open(f"{ptm}.txt", "r") as file:
        read_data = file.read()
        data1 = read_data.split("\n")
        data2 = read_data.split("\n")
        for line in data1:
            if "ATOM" in line and "ATOM H" not in line:
                single_bonds = []
                double_bonds = []
                atom = line.split()[1]
                #print(atom)
                for line2 in data2:
                    if "BOND" in line2:
                        # to remove newline characters causing every odd line to be blank (starting from 0)
                        strip_line2 = line2.strip()
                        split_line2 = strip_line2.split()
                        split_line2.pop(0)
                        #print(split_line2)
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
                all_connections.append(connections)
    file.close()
    #print(all_connections)
    return all_connections


#                 edited_ptm_file = figure_out_atom_type(ptm, connections, atom, edited_ptm_file)
#     file.close
#     return edited_ptm_file

def grouped(iterable, n):
    # iterate each two values (two atoms that have a bond)
    return zip(*[iter(iterable)]*n)

def figure_out_atom_type(ptm, all_connections):
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
                            "['C', ['CA', '+N'], ['O']]" : "C",
                            "['O', [], ['C']]" : "O",
                            "['CB', ['CA', 'OG'], []]" : "CT2",
                            "['OG', ['CB'], []]" : "OH1"
                            }
    atoms = []
    for atom_connection in all_connections:
        atoms.append(atom_connection[0])

    # Turn list into string so it can be searched as a key (key in dictionary can't be a list)
    str_all_connections = str(all_connections)
    #print(f"{connections} -- {atom_type_replacement[connections]}")
    data = ""
    with open(f"{ptm}.txt", "r") as ptm_file:
        for line in ptm_file:
            counter = 0
            for atom in atoms:
                if f"ATOM {atom} " in line:
                    replacement = list(atom_type_replacement.keys())[counter]
                    remove_spaces = False
                    atom_type_to_be_replaced = line.split()[2]
                    if len(atom_type_to_be_replaced) > len(replacement):
                        difference = len(atom_type_to_be_replaced) - len(replacement)
                        final_atom_type = replacement + ' ' * difference
                    elif len(atom_type_to_be_replaced) < len(replacement):
                        difference = len(replacement) - len(atom_type_to_be_replaced)
                        final_atom_type = replacement
                        remove_spaces = True
                    # Searching and replacing the text using the replace() function
                    # The same index in boths list are synonyms
                    else:
                        final_atom_type = replacement
                    if remove_spaces == True:
                        line = line.replace(atom_type_to_be_replaced + difference * " ", final_atom_type)
                    else:
                        line = line.replace(atom_type_to_be_replaced, final_atom_type)
                        
                    data += line
                else:
                    counter += 1
                       
    print(data)
    # with open(f"{ptm}_edited.txt", "w") as edited_ptm_file:
    #     edited_ptm_file.write(data)
    # edited_ptm_file.close
    # return edited_ptm_file


# def append_to_top_heav_lib(edited_ptm_file, ptm):
#     # Opening our text file in write only mode to write the replaced content
#     #with open('/home/shahielm/Automate/top_heav,lib', 'a') as appendfile:
#     with open(f"{ptm}_edited.txt", "r") as ptm_file:
#         in_data = ptm_file.read()
#     ptm_file.close()
#     with open('/home/shahielm/Automate/practice_output_file.txt', 'a') as appendfile:
#         # Writing the replaced data in our text file
#         appendfile.write("\n\n")
#         appendfile.write(in_data)
#         print("Text replaced")    
    

ptms = ["ARG", "SER"]
for ptm in ptms:
    obtain_seperate_rtf(ptm)
    all_connections = find_atom_connections(ptm)
    figure_out_atom_type(ptm, all_connections)
    # append_to_top_heav_lib(edited_ptm_file, ptm)
