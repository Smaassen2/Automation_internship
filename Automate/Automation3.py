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
        in_data = file.read()
        file1 = in_data.split("\n")
        file2 = in_data.split("\n")
        for line in file1:
            if "ATOM" in line and "ATOM H" not in line:
                single_bonds = []
                double_bonds = []
                atom = line.split()[1]
                #print(atom)
                for line2 in file2:
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
                edited_ptm_file = figure_out_atom_type(ptm, connections, atom)
    file.close
    return edited_ptm_file

def grouped(iterable, n):
    # iterate each two values (two atoms that have a bond)
    return zip(*[iter(iterable)]*n)

def figure_out_atom_type(ptm, connections, atom):
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
    connections = str(connections)
    #print(f"{connections} -- {atom_type_replacement[connections]}")
    replacement = atom_type_replacement[connections]

    with open(f"{ptm}_update.txt", "r") as edited_ptm_file:
        for line in edited_ptm_file:
            if f"ATOM {atom} " in line:
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
    edited_ptm_file.close
    return edited_ptm_file


def append_to_top_heav_lib(edited_ptm_file, ptm):
    # Opening our text file in write only mode to write the replaced content
    #with open('/home/shahielm/Automate/top_heav,lib', 'a') as appendfile:
    with open(f"{ptm}.txt", "r") as ptm_file:
        in_data = ptm_file.read()
    ptm_file.close()
    with open('/home/shahielm/Automate/practice_output_file.txt', 'a') as appendfile:
        # Writing the replaced data in our text file
        appendfile.write("\n\n")
        appendfile.write(in_data)
        print("Text replaced")    
    

ptms = ["ARG"]
for ptm in ptms:
    obtain_seperate_rtf(ptm)
    edited_ptm_file = find_atom_connections(ptm)
    append_to_top_heav_lib(edited_ptm_file, ptm)
