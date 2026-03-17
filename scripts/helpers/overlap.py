import subprocess
import sys

methods = ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]
build = sys.argv[1]

base_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/"
buff_loc = base_loc + "buff"
overlap_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/overlap_" + build + ".txt"

overlap = []
for x in methods:
    for y in methods:
        buff = {}
        x_loc = base_loc + x + ".gtf"
        y_loc = base_loc + y + ".gtf"

        bedtools_call = "bedtools intersect -wo -a " + x_loc + " -b " + y_loc + " -f 0.25 -r > " + buff_loc

        subprocess.call(bedtools_call, shell=True)

        with open(buff_loc, "r")  as f:
            for line in f.readlines():
                name = line.strip().split()[11][1:-2]
                rank = line.strip().split()[-1]
                if name not in buff:
                    buff[name] = rank
        overlap += [[x, y, str(len(buff.keys()))]]
        print(overlap)

with open(overlap_loc, "w") as f:
    for o in overlap:
        f.write(",".join(o) + "\n")
