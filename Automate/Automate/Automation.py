def obtain_seperate_rtf(ptm):
    info = ""
    with open("/home/shahielm/toppar/stream/prot/toppar_all36_prot_modify_res.str", "r") as k:
        part_of_ptm = False
        for line in k:
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
                "NG2S2" : "NH2  ",
                "HB1" : "HB ",
                "H " : "HB"}

    # Opening our text file in read only
    # mode using the open() function
    with open(f"{ptm}.txt", "r") as file:

        # Reading the content of the file
        # using the read() function and storing
        # them in a new variable
        data = file.read()

        # Searching and replacing the text
        # using the replace() function
        # The same index in boths list are synonyms
        for atom_type in dictionary:
            data = data.replace(atom_type, dictionary[atom_type])

    # Opening our text file in write only
    # mode to write the replaced content
    with open('/home/shahielm/Automate/top_heav,lib', 'a') as file:

        # Writing the replaced data in our
        # text file
        file.write(f"\n\n{data}")

    # Printing Text replaced
    print("Text replaced")

ptms = ["CIR"]
for ptm in ptms:
    obtain_seperate_rtf(ptm)
    update_atom_type_names(ptm)