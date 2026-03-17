import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

in_folder = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/"
in_counts = in_folder + "tespex/" + sample + "/outfile.txt"
out_counts = in_folder + "sim/" + sample + "/counts/tespex.txt"



with open(in_counts, "r") as f:
    lines = f.readlines()
    for l in lines[1:]:
        buff = l.strip().split()
        print(buff)
        buff[0] = buff[0].replace("#", "/")
        count = buff[1]
        buff = buff[0].split("/")
        
        print(buff)
        quit()

counts = sorted([[x[0], str(x[1])] for x in list(counts.items())])

with open(out_counts, "w") as f:
    for x in counts:
        buff = ",".join(x) + "\n"
        f.write(buff)
