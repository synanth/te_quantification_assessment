import sys

build = sys.argv[1]
gtf = sys.argv[2]

gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/" + gtf + ".gtf"
len_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/" + gtf + ".len"


lens = []
with open(gtf_loc, "r") as f:
    lines = f.readlines()
    for l in lines:
        buff = l.strip().split()
        lens += [int(buff[4]) - int(buff[3])]

with open(len_loc, "w") as f:
    for l in lens:
        f.write(str(l) + "\n")
