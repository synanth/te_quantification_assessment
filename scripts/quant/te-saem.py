import os
import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_de = sys.argv[4]
depth = sys.argv[5]
n_cpu = str(32)


working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/"
program_loc = "/home/stexocae/li_lab/saem/te-saem.py"
ref_path = "/lustre/stexocae/li_lab/saem/refs/"

if build == "chm13":
    gtf_loc = ref_path + "hs1.gtf"
elif build == "hg38":
    gtf_loc = ref_path + "hg38.gtf"
else:
    sys.exit("Only hg38 or chm13 work for now")

sample_loc = working_dir + "sim/" + sample + "/"
out_loc = working_dir + "te-saem/" + sample + "/"
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/te-saem.py"

mkdir_call = "mkdir " + out_loc

te_saem_call  = "python3 " + program_loc + " "
te_saem_call += "-t " + n_cpu + " " 
te_saem_call += "-1 " + sample_loc + sample + "_1.fasta " 
te_saem_call += "-2 " + sample_loc + sample + "_2.fasta "
te_saem_call += "-o " + out_loc + sample + "_counts.csv"

print(te_saem_call)
print(mkdir_call)
subprocess.run(mkdir_call, shell=True)
subprocess.run(te_saem_call, shell=True)


## translate ##
translate_call = "python3 " + translate_loc + " " + build + " " + gtf + " " + sample + " " + n_de + " " + depth
subprocess.run(translate_call, shell=True)

## clean up ##
#rm_call = "rm -rf " + out_loc
#subprocess.run(rm_call, shell=True)
