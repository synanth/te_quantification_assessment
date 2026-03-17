import os
import sys
import subprocess

srr = sys.argv[1]
n_cpu = str(16)


working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
program_loc = "/home/stexocae/li_lab/saem/te-saem.py"
ref_path = "/lustre/stexocae/li_lab/saem/refs/"

gtf_loc = ref_path + "hs1.gtf"

out_loc = working_dir + "te-saem/"

mkdir_call = "mkdir " + out_loc

te_saem_call  = "python3 " + program_loc + " "
te_saem_call += "-t " + n_cpu + " " 
te_saem_call += "-1 " + working_dir + srr+ "_1.fastq " 
te_saem_call += "-2 " + working_dir + srr + "_2.fastq "
te_saem_call += "-o " + out_loc + srr + "_counts.csv"

print(te_saem_call)
print(mkdir_call)
subprocess.run(mkdir_call, shell=True)
subprocess.run(te_saem_call, shell=True)

## translate ##
raw_counts_loc = out_loc + srr + "_counts.csv"
final_counts_loc = out_loc + "final_counts.csv"
out_csv = []

with open(raw_counts_loc, "r") as f:
    lines= f.readlines()
    for line in lines:
        buff = line.strip().split(",")
        out_csv += [[buff[0], buff[1]]]
with open(final_counts_loc, "w") as f:
    for line in out_csv:
        f.write(line[0] + "," + line[1] + "\n")
