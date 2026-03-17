## This program runs SQuIRE

import sys
import subprocess


## parameters ##
build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_de = sys.argv[4]
depth = sys.argv[5]


## file management ##
working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/sim/" + sample + "/"
squire_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/squire/"  
package_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/SQuIRE/squire/"
map_loc = package_loc + "Map.py"
count_loc = package_loc + "Count.py"
fetch_loc = package_loc + "squire_fetch/"
clean_loc = package_loc + "squire_clean/"
star_loc = squire_dir + sample + "/star"
quant_loc = squire_dir + sample + "/quant/"
read1_loc = working_dir + sample + "_1.fasta"
read2_loc = working_dir + sample + "_2.fasta"


## construct call ##
if build == "chm13":
    squire_map_call = "python " + map_loc + " -b hs1 -v -p 8 -r 100"
elif build == "hg38":
    squire_map_call = "python " + map_loc + " -b hg38 -v -p 32 -r 100"
else:
    sys.exit("Build must be hg38 or chm13")
squire_map_call += " -f " + fetch_loc
squire_map_call += " -1 " + read1_loc + " -2 " + read2_loc 
squire_map_call += " -o " + star_loc + " -n " + sample

if build == "chm13":
    squire_count_call = "python " + count_loc + " -b hs1 -v -p 8 -r 100 "
elif build == "hg38":
    squire_count_call = "python " + count_loc + " -b hg38 -v -p 8 -r 100 "
else:
    sys.exit("Build must be hg38 or chm13")
squire_count_call += " -m " + star_loc + " -f " + fetch_loc
squire_count_call += " -o " + quant_loc + " -n " + sample
squire_count_call += " -c " + clean_loc

subprocess.run(squire_map_call, shell=True)
subprocess.run(squire_count_call, shell=True)


## translate ##
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/squire.py"
translate_call = "python3 " + translate_loc + " " + build + " " + gtf + " " + sample + " " + n_de + " " + depth

subprocess.run(translate_call, shell=True)

## clean up ##
#rm_call = "rm -rf " + squire_dir + "*"
