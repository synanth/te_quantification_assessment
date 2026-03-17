## This program runs SQuIRE

import sys
import subprocess


## parameters ##
srr = sys.argv[1]

## file management ##
working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
squire_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/squire/"  
package_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/SQuIRE/squire/"
map_loc = package_loc + "Map.py"
count_loc = package_loc + "Count.py"
fetch_loc = package_loc + "squire_fetch/"
clean_loc = package_loc + "squire_clean/"
star_loc = squire_dir + srr + "/star"
quant_loc = squire_dir + srr + "/quant/"
read1_loc = working_dir + srr + "_1.fastq"
read2_loc = working_dir + srr + "_2.fastq"


## construct call ##
squire_map_call = "python " + map_loc + " -b hs1 -v -p 8 -r 100"
squire_map_call += " -f " + fetch_loc
squire_map_call += " -1 " + read1_loc + " -2 " + read2_loc 
squire_map_call += " -o " + star_loc + " -n " + srr

squire_count_call = "python " + count_loc + " -b hs1 -v -p 8 -r 100 "
squire_count_call += " -m " + star_loc + " -f " + fetch_loc
squire_count_call += " -o " + quant_loc + " -n " + srr
squire_count_call += " -c " + clean_loc

subprocess.run(squire_map_call, shell=True)
subprocess.run(squire_count_call, shell=True)

## translate ##
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/squire.gtf"
raw_counts_loc = squire_dir + srr + "/quant/" + srr + "_TEcounts.txt"
final_counts_loc = squire_dir + "final_counts.csv"
bed_loc = squire_dir + srr + ".bed"
bedtools_out_loc = squire_dir + srr + ".bedtools.out"
out_bed = []
counts = []

with open(raw_counts_loc, "r") as f:
    lines = f.readlines()[1:]
    for line in lines:
        buff = line.strip().split()
        buff2 = buff[3].split("|")
        out_bed += [[buff2[0], buff2[1], buff2[2], buff[-2]]]

with open(bed_loc, "w") as f:
    for line in out_bed:
        f.write("\t".join(line) + "\n")

bedtools_call = "bedtools intersect -f 0.25 -r -wo -a " + bed_loc + " -b " + gtf_loc + " > " + bedtools_out_loc
subprocess.run(bedtools_call, shell=True)

with open(bedtools_out_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        counts += [[buff[15][1:-2], buff[3]]]


with open(final_counts_loc, "w") as f:
    for line in counts:
        f.write(line[0] + "," + line[1] + "\n")
