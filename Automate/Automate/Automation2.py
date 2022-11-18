def obtain_seperate_rtf(ptm):
    info = ""
    with open("/home/shahielm/toppar/stream/prot/toppar_all36_prot_modify_res.str", "r") as file:
        part_of_ptm = False
        for line in file:
            if f"RESI {ptm}" in line:
                part_of_ptm = True
                info = line
            elif "RESI" in line or "PRES" in line:
                part_of_ptm = False
            elif part_of_ptm == True:
                if "DOUBLE" in line:
                    # will not work on acetylated lysine because the makers of toppar_all36_prot_modify_res.str accidentally wrote "DOUB" instead of "DOUBLE"  <-- So it is not a mistake on my part.
                    line = line.replace("DOUBLE", "BOND  ")
                info += line
            
    file.close()            
    with open(f"{ptm}.txt", "w") as output:
        output.write(info)
        output.truncate(output.tell()-2)
    output.close()
    return ptm

def find_atom_connections(ptm):
    connections = {}
    with open(f"{ptm}.txt", "r") as file:
        for line in file:
            if "BOND" in line:
                # to remove newline characters causing every odd line to be blank (starting from 0)
                strip_line = line.strip()
                split_line = strip_line.split()
                split_line.pop(0)
                for x, y in grouped(split_line, 2):
                    if x not in connections:
                        connections[x] = [y]
                    else:
                        connections[x].append(y)

                    if y not in connections:
                        connections[y] = [x]
                    else:
                        connections[y].append(x)

    file.close()
    return connections
    
def grouped(iterable, n):
    # iterate each two values (two atoms that have a bond)
    return zip(*[iter(iterable)]*n)

def figure_out_atom_type(ptm, connections):
    atom_type_replacement = {"['N', ['CA', 'HN']]" : "NH1",
                            "['CA', ['N', 'C', 'HA', 'CB']]" : "CT1",
                            "['C', ['CA', '+N', 'O']]" : "C",
                            "['HA', ['CA']]" : "HB",
                            "['CB', ['CA', 'HB1', 'HB2', 'CG']]" : "CT2",
                            "['HN', ['N']]" : "HB",
                            "['HB1', ['CB']]" : "HA",
                            "['HB2', ['CB']]" : "HA",
                            "['CG', ['CB', 'HG2', 'HG1', 'CD']]" : "CT2",
                            "['HG2', ['CG']]" : "HA",
                            "['HG1', ['CG']]" : "HA",
                            "['CD', ['CG', 'HD1', 'HD2', 'NE']]" : "CT2",
                            "['HD1', ['CD']]" : "HA",
                            "['HD2', ['CD']]" : "HA",
                            "['NE', ['CD', 'HE', 'CZ']]" : "NH1",
                            "['HE', ['NE']]" : "HA",
                            "['CZ', ['NE', 'NH', 'OH']]" : "C",
                            "['NH', ['CZ', 'HH1', 'HH2']]" : "NH2",
                            "['HH1', ['NH']]" : "HA",
                            "['HH2', ['NH']]" : "HA",
                            "['O', ['C']]" : "O",
                            "['OH', ['CZ']]" : "O"}
    atom_connections = []
    with open(f"{ptm}.txt", "r") as readfile:
        # Reading the content of the file
        # using the read() function and storing
        # them in a new variable
        data = readfile.read()

    for connection in connections:
        atom_connections.append([connection, connections[connection]])
        
    for atom in atom_connections:
        atom_need_atom_type_replacement = atom[0]
        str_atom = str(atom)

        if str_atom.startswith("['+N'") == False:
            replacement = (atom_type_replacement[str_atom])
            data = modify_data(ptm, atom_need_atom_type_replacement, replacement, data)
    return data

def modify_data(ptm, atom_need_atom_type_replacement, replacement, data):
    for line in data.split("\n"):
        if f"ATOM {atom_need_atom_type_replacement} " in line:
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
                line2 = line.replace(atom_type_to_be_replaced + difference * " ", final_atom_type)
            else:
                line2 = line.replace(atom_type_to_be_replaced, final_atom_type)
            data = data.replace(line, line2)

    return data

def write_to_top_heav_lib(data):
    # Opening our text file in write only mode to write the replaced content
    with open('/home/shahielm/Automate/top_heav,lib', 'a') as appendfile:
        # Writing the replaced data in our text file
        appendfile.write(f"\n\n{data}")
            
    

ptms = ["CIR"]
for ptm in ptms:
    obtain_seperate_rtf(ptm)
    connections = find_atom_connections(ptm)
    data = figure_out_atom_type(ptm, connections)
    #print(data)
    write_to_top_heav_lib(data)


























# def obtain_seperate_rtf(ptm):
#     info = ""
#     with open("/home/shahielm/toppar/stream/prot/toppar_all36_prot_modify_res.str", "r") as file:
#         part_of_ptm = False
#         for line in file:
#             if f"RESI {ptm}" in line:
#                 part_of_ptm = True
#                 info = line
#             elif "RESI" in line or "PRES" in line:
#                 part_of_ptm = False
#             elif part_of_ptm == True:
#                 if "DOUBLE" in line:
#                     # will not work on acetylated lysine because the makers of toppar_all36_prot_modify_res.str accidentally wrote "DOUB" instead of "DOUBLE"  <-- So it is not a mistake on my part.
#                     line = line.replace("DOUBLE", "BOND  ")
#                 info += line
            
                
#     with open(f"{ptm}.txt", "w") as output:
#         output.write(info)
#         output.truncate(output.tell()-2)

#     return ptm

# def find_atom_connections(ptm):
#     connections = {}
#     with open(f"{ptm}.txt", "r") as file:
#         for line in file:
#             if "BOND" in line:
#                 # to remove newline characters causing every odd line to be blank (starting from 0)
#                 strip_line = line.strip()
#                 split_line = strip_line.split()
#                 split_line.pop(0)
#                 for x, y in grouped(split_line, 2):
#                     if x not in connections:
#                         connections[x] = [y]
#                     else:
#                         connections[x].append(y)

#                     if y not in connections:
#                         connections[y] = [x]
#                     else:
#                         connections[y].append(x)

#     # for connection in connections:
#     #     print(f"{connection} {connections[connection]}")

#     return connections
    
# def grouped(iterable, n):
#     # iterate each two values (two atoms that have a bond)
#     return zip(*[iter(iterable)]*n)

# def figure_out_atom_type(ptm, connections):
#     atom_type_replacement = {"['N', ['CA', 'HN']]" : "NH1",
#                             "['CA', ['N', 'C', 'HA', 'CB']]" : "CT1",
#                             "['C', ['CA', '+N', 'O']]" : "C",
#                             "['HA', ['CA']]" : "HB",
#                             "['CB', ['CA', 'HB1', 'HB2', 'CG']]" : "CT2",
#                             "['HN', ['N']]" : "HB",
#                             "['HB1', ['CB']]" : "HA",
#                             "['HB2', ['CB']]" : "HA",
#                             "['CG', ['CB', 'HG2', 'HG1', 'CD']]" : "CT2",
#                             "['HG2', ['CG']]" : "HA",
#                             "['HG1', ['CG']]" : "HA",
#                             "['CD', ['CG', 'HD1', 'HD2', 'NE']]" : "CT2",
#                             "['HD1', ['CD']]" : "HA",
#                             "['HD2', ['CD']]" : "HA",
#                             "['NE', ['CD', 'HE', 'CZ']]" : "NH1",
#                             "['HE', ['NE']]" : "HA",
#                             "['CZ', ['NE', 'NH', 'OH']]" : "C",
#                             "['NH', ['CZ', 'HH1', 'HH2']]" : "NH2",
#                             "['HH1', ['NH']]" : "HA",
#                             "['HH2', ['NH']]" : "HA",
#                             "['O', ['C']]" : "O",
#                             "['OH', ['CZ']]" : "O"}
#     atom_connections = []
#     for connection in connections:
#         atom_connections.append([connection, connections[connection]])
        
#     for atom in atom_connections:
#         atom_need_atom_type_replacement = atom[0]
#         str_atom = str(atom)
#         if str_atom.startswith("['+N'") == False:
#             replacement = (atom_type_replacement[str_atom])
#             write_in_ptm_file(ptm, atom_need_atom_type_replacement, replacement)
    

# def write_in_ptm_file(ptm, atom_need_atom_type_replacement, replacement):
#     with open(f"{ptm}.txt", "r") as readfile:

#         # Reading the content of the file
#         # using the read() function and storing
#         # them in a new variable
#         N = 3
#         for line in readfile:
#             if line.startswith("ATOM") and atom_need_atom_type_replacement in line:
#                 atom_type_to_be_replaced = line.split()[2]
#                 print(atom_type_to_be_replaced)
#                 if len(atom_type_to_be_replaced) > len(replacement):
#                     difference = len(atom_type_to_be_replaced) - len(replacement)
#                     final_atom_type = replacement + ' ' * difference
#                 if len(atom_type_to_be_replaced) < len(replacement):
#                     difference = len(replacement) - len(atom_type_to_be_replaced)
#                     final_atom_type = replacement + '\b' * difference
                
        
#                 # Searching and replacing the text using the replace() function
#                 # The same index in boths list are synonyms
#                 line = line.replace(atom_type_to_be_replaced, final_atom_type)
        
#                 # Opening our text file in write only mode to write the replaced content
#                 with open('/home/shahielm/Automate/top_heav,lib', 'a') as appendfile:
#                     # Writing the replaced data in our text file
#                     appendfile.write(f"\n\n{data}")
            
    

# ptms = ["CIR"]
# for ptm in ptms:
# #    obtain_seperate_rtf(ptm)
#     connections = find_atom_connections(ptm)
#     figure_out_atom_type(ptm, connections)
# #    update_atom_type_names(ptm)
