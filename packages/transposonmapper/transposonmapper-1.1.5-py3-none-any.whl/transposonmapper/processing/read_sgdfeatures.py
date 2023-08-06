# -*- coding: utf-8 -*-

from transposonmapper.importing import load_sgd_tab
from transposonmapper.utils   import  chromosomename_roman_to_arabic

def sgd_features(filepath=None):
    """This function read the file SGD_features.tab and create a dictionary with useful info for processing

    Parameters
    ----------
    filepath : str, optional
        filepath of the sgd.tab file , by default None

    Returns
    -------
    dict
         A dictionary with the following info: 
        key:
            0. Feature name
        value:
            0. feature type (l[1])
            1. feature qualifier (Verified or Dubious) (l[2])
            2. Standard name (l[4])
            3. Aliases (separated by '|') (l[5])
            4. Parent feature name (typically 'chromosome ...') (l[6])
            5. Chromosome (l[8])
            6. start coordinate (starting at 0 for each chromosome) (l[9])
            7. end coordinate (starting at 0 for each chromosome) (l[10])
           
            This file reads the SGD_features.txt file found at http://sgd-archive.yeastgenome.org/curation/chromosomal_feature/
    """

    if filepath == None:
        filepath=load_sgd_tab()

    arabic_to_roman_dict=chromosomename_roman_to_arabic()[0]
    
    with open(filepath) as f:
        lines = f.readlines()


    feature_list = []
    feature_orf_dict = {}
    feature_ars_dict = {}
    feature_telomere_dict = {}
    feature_ltr_dict = {}
    feature_centromere_dict = {}
    feature_Xelement_dict = {}
    feature_intron_dict = {}
    feature_ncrna_dict = {}
    feature_ncexon_dict = {}
    feature_trna_dict = {}
    feature_snorna_dict = {}
    feature_teg_dict = {}
    feature_5p_utrintron_dict = {}
    feature_mas_dict = {}
    feature_snrna_dict = {}
    feature_rrna_dict = {}
    feature_ets_dict = {}
    feature_its_dict = {}
    feature_oor_dict = {}
    feature_telrna_dict = {}
    
    for line in lines:
        l = line.strip('\n').split('\t')
        if not l[1] in feature_list:
            feature_list.append(l[1])

        if not l[8].endswith('micron') and not l[8] == '':
            chromosome = arabic_to_roman_dict.get(int(l[8]))
            if l[1] == 'ORF':
                feature_orf_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'ARS':
                feature_ars_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'telomere':
                feature_telomere_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'long_terminal_repeat':
                feature_ltr_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'centromere':
                feature_centromere_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'X_element':
                feature_Xelement_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'intron':
                feature_intron_dict[l[6]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'ncRNA_gene':
                feature_ncrna_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'noncoding_exon':
                feature_ncexon_dict[l[6]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'tRNA_gene':
                feature_trna_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'snoRNA_gene':
                feature_snorna_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'transposable_element_gene':
                feature_teg_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'five_prime_UTR_intron':
                feature_5p_utrintron_dict[l[6]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'matrix_attachment_site':
                feature_mas_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'snRNA_gene':
                feature_snrna_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'rRNA_gene':
                feature_rrna_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'external_transcribed_spacer_region':
                feature_ets_dict[l[6]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'internal_transcribed_spacer_region':
                feature_its_dict[l[6]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'origin_of_replication':
                feature_oor_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]
            elif l[1] == 'telomerase_RNA_gene':
                feature_telrna_dict[l[3]] = [l[1], l[2], l[4], l[5], l[6], chromosome, l[9],l[10]]


    


    genomicregions_list = ['ORF', 'ARS', 'Telomere', 'long_terminal_repeat',
                           'Centromere', 'X_element', 'Intron', 'ncRNA_gene',
                           'Noncoding_exon', 'tRNA_gene', 'snoRNA_gene',
                           'transposable_element_gene', 'five_prime_UTR_intron',
                           'matrix_attachment_site', 'snRNA_gene', 'rRNA_gene',
                           'external_transcribed_spacer_region',
                           'internal_transcribed_spacer_region',
                           'origin_of_replication', 'telomerase_RNA_gene']


    return(genomicregions_list, feature_orf_dict, feature_ars_dict, feature_telomere_dict,
           feature_ltr_dict, feature_centromere_dict, feature_Xelement_dict, feature_intron_dict,
           feature_ncrna_dict, feature_ncexon_dict, feature_trna_dict,
           feature_snorna_dict, feature_teg_dict, feature_5p_utrintron_dict,
           feature_mas_dict, feature_snrna_dict, feature_rrna_dict,
           feature_ets_dict, feature_its_dict, feature_oor_dict,
           feature_telrna_dict)


