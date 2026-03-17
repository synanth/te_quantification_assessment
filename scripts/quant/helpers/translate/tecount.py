import sys
import subprocess
from operator import itemgetter

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

in_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/tecount/" + sample + "/TEtranscripts_out.cntTable"
out_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/" + sample + "/counts/tecount.txt"
sim_counts_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/sim_counts_matrix.csv"
sim_gtf_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/subset.gtf"

if gtf == "superset" or gtf == "herv" or gtf == "line":
    translation_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/tecount_to_superset.txt"
elif gtf != "tecount":
    translation_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/tecount_to_" + gtf + ".txt"

    


translation = {}
counts = {}
unrepresented = 0
with open(translation_loc, "r") as f:
    lines = f.readlines()
    for l in lines:
        buff = l.strip().split(",")
        translation[buff[0]] = buff[1]

with open(sim_counts_loc, "r") as f:
    lines = f.readlines()
    for l in lines[1:]:
        buff = l.strip().split(",")
        counts[buff[0]] = 0

with open(in_counts, "r") as f:
    lines = f.readlines()
    for l in lines[46000:]:
        buff = l.strip().split()
        if buff[0] in translation.values():
            counts[translation[buff[0]]] += int(buff[1])
        else:
            counts["unrepresented"] += int(buff[1])
counts = sorted(list(counts.items()))


with open(out_loc, "w") as f:
    f.write("name,count" + "\n")
    for x in counts:
        name = x[0]
        count = str(x[1])
        f.write(name + "," + count + "\n")
