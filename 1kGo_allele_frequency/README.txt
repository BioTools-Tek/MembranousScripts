This is a series of scripts for finding the Odds Ratios for given
snps across all 1kGo individuals.

It attempts to recreate the Table3 from the 2011_NEJM_Stanescu_Kleta 
paper.


#1 Input file: chr, snpname
#2 Assert that VCF files have the same ID list if on different 
   chromosomes.
#3 Extract genotypes for said SNPs in input file
#4 Sort into groups
#5 Count
