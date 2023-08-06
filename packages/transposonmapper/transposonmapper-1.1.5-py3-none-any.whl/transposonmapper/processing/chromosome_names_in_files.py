import os
def chromosome_name_bedfile(bed_file):
    '''This function returns some properties of the chromosomes in a bed file.
    Input can be either of two options:
        The full path to a bed file after which the program opens the bed file, or
        a list of the lines in the bed file. The latter requires to read the bed file before calling this function and input all lines in the bed file as a list. The function than does not open the bed file again.
    Returns three dictionaries (in this order):
        The first indicates the names of the chromosomes as used in the bed file (keys are roman numerals 1 to 16 and the values are the names used in the bed file).
        The second is the start line in the bed file of each chromosome (keys are the roman numerals of the chromosome names and the values are the start lines in the bed file of the chromosome).
        The third is the end line in the bed file of each chromosome (keys are the roman numerals of the chromosome names and the values are the start lines in the bed file of the chromosome)

    CHANGE LINE 60 AND 71 TO AUTOMATICALLY RECOGNIZE THE MITOCHONDRIAL DNA NAME
    '''
    
    
    if type(bed_file) is str:
        
        assert os.path.isfile(bed_file), "ERROR: bed file not found"
        with open(bed_file) as f:
            lines = f.readlines()
    elif type(bed_file) is list:
        lines = bed_file




    num_arabic = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    num_roman = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI']
    roman_to_arabic_dict = {}
    index_counter = 0
    for rom in num_roman:
        roman_to_arabic_dict[rom] = num_arabic[index_counter]
        index_counter += 1

    chromosome_romannames_list = []
    for roman in roman_to_arabic_dict:
        chromosome_romannames_list.append(roman)




    chrom_names_dict = {}
    chrom_start_line_dict = {}
    chrom_end_line_dict = {}

    chrom_name_in_bed = ''
    chr_counter = 0
    line_counter = 0
    stop_loop = False
    while stop_loop is False:
        line = lines[line_counter]
        chrom_name_current = line.split(' ')[0].replace('chr','')
        if not chrom_name_current.startswith('track') and not chrom_name_current.startswith('M') and not chrom_name_current.startswith('ref|NC_001224|') and chr_counter < 16: #SKIP HEADER AND MITOCHRONDRIAL CHROMOSOMES #and not chrom_name_current.startswith('M')
            if chrom_name_current != chrom_name_in_bed:
                chrom_names_dict[chromosome_romannames_list[chr_counter]] = chrom_name_current
                chrom_name_in_bed = chrom_name_current
#                print('Chromosome ',chromosome_romannames_list[chr_counter], 'is ',chrom_name_current)
                
                chrom_start_line_dict[chromosome_romannames_list[chr_counter]] = line_counter #GET START INDEX IN THE BED FILE OF THE CURENT CHROMOSOME
                if chr_counter != 0:
                    chrom_end_line_dict[chromosome_romannames_list[chr_counter-1]] = line_counter-1 #GET THE END INDEX IN THE BED OF THE PREVIOUS CHROMOSOME (SKIP FOR THE FIRST CHROMOSOME)

                chr_counter += 1

        elif chrom_name_current.startswith('M') or chrom_name_current.startswith('ref|NC_001224|'):
            chrom_end_line_dict[chromosome_romannames_list[-1]] = line_counter-1 #GET THE END INDEX IN THE BED FILE FOR THE FINAL CHROMOSOME
            stop_loop = True
                
        line_counter += 1
        
    return(chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict)

#%%
def chromosome_name_wigfile(wig_file):

    if type(wig_file) is str:
      
        assert os.path.isfile(wig_file), "ERROR: wig file not found"
        with open(wig_file) as f:
            lines = f.readlines()
    elif type(wig_file) is list:
        lines = wig_file




    num_arabic = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    num_roman = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','M']
    roman_to_arabic_dict = {}
    index_counter = 0
    for rom in num_roman:
        roman_to_arabic_dict[rom] = num_arabic[index_counter]
        index_counter += 1

    chromosome_romannames_list = []
    for roman in roman_to_arabic_dict:
        chromosome_romannames_list.append(roman)





    chrom_names_dict = {}
    chrom_start_line_dict = {}
    chrom_end_line_dict = {}

    chr_counter = 0
    line_counter = 0
    chrom_line = 'variablestep'
    for line in lines:
        line.strip('\n')
        line_split = line.split(' ')
        if line_split[0].lower() == chrom_line and chr_counter < 17:
            chromosome_name = line_split[1].replace('chrom=chr','').strip('\n')
            chrom_names_dict[chromosome_romannames_list[chr_counter]] = chromosome_name
#            print('Chromosome ',chromosome_romannames_list[chr_counter], 'is ',chromosome_name)
            
            chrom_start_line_dict[chromosome_romannames_list[chr_counter]] = line_counter+1 #GET START INDEX IN THE BED FILE OF THE CURENT CHROMOSOME
            if chr_counter != 0:
                chrom_end_line_dict[chromosome_romannames_list[chr_counter-1]] = line_counter #GET THE END INDEX IN THE BED OF THE PREVIOUS CHROMOSOME (SKIP FOR THE FIRST CHROMOSOME)

            chr_counter += 1
        line_counter += 1

    chrom_end_line_dict[chromosome_romannames_list[chr_counter-1]] = len(lines)


    return(chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict)

# #%%
# if __name__ == '__main__':
#     chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict = chromosome_name_bedfile(bed_file=r"")
#     # chrom_names_dict, chrom_start_line_dict, chrom_end_line_dict = chromosome_name_wigfile(wig_file=r"")