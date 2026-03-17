import os
import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
n_de = sys.argv[3]
depth = sys.argv[4]
input_folder = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/"
samples = list(set([x[:9] for x in os.listdir(input_folder) if "fasta" in x]))
print(samples)

#methods = ["bowtie2", "star"]
methods = ["star"]


## clean up old data ##
for x in methods:
    rm_data_call = "rm -rf " + input_folder + x + "/*"
    rm_out_logs_call = "rm -rf " + "out/align/" + x + "/*"
    subprocess.call(rm_data_call, shell=True)
    subprocess.call(rm_out_logs_call, shell=True)
    print(rm_data_call)
    print(rm_out_logs_call)


## call alignment algos based upon methods list ##

for x in methods:
    for y in samples:
        star_call = ["bash",  "scripts/slurm/" + x + ".sh", y, gtf, n_de, depth]
        s = subprocess.check_output(star_call).decode("utf-8")
        print(s)
