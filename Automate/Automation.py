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
            
                
    with open(f"{ptm}.txt", "w") as output:
        output.write(info)
        output.truncate(output.tell()-2)

    return ptm

def update_atom_type_names(ptm):
    dictionary = {"CG321": "CT2  ", 
                "HGA2" : "HA  ", 
                "NG2S1" : "NH1  ", 
                "HGP1" : "HA  ", 
                "CG2O6" : "C    ", 
                "OG2D1" : "O    ", 
                "NG2S2" : "NH2  "}

    # Opening our text file in read only
    # mode using the open() function
    with open(f"{ptm}.txt", "r") as readfile:
    
        # Reading the content of the file
        # using the read() function and storing
        # them in a new variable
        data = readfile.read()
    
        # Searching and replacing the text
        # using the replace() function
        # The same index in boths list are synonyms
        for atom_type in dictionary:
            data = data.replace(atom_type, dictionary[atom_type])
    
    # Opening our text file in write only
    # mode to write the replaced content
    with open('/home/shahielm/Automate/top_heav,lib', 'a') as appendfile:
    
        # Writing the replaced data in our
        # text file
        appendfile.write(f"\n\n{data}")
    
    # Printing Text replaced
    print("Text replaced")

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
                    #connections[y] = x
                    #print(f"{x} -- {y}")
                #print(split_line)
    for connection in connections:
        print(f"{connection} {connections[connection]}")

    return connections
    
def grouped(iterable, n):
    return zip(*[iter(iterable)]*n)

def figure_out_atom_type(ptm, connections):
     with open(f"{ptm}.txt", "r") as file:
        for line in file:
            if "ATOM" in line:
                split_line = line.split()
                for atom in connections:
                    if atom == split_line[1]:
                        split_line[2] = 
                print(split_line)

ptms = ["CIR"]
for ptm in ptms:
#    obtain_seperate_rtf(ptm)
    connections = find_atom_connections(ptm)
    figure_out__atom_type(ptm, connections)
#    update_atom_type_names(ptm)


