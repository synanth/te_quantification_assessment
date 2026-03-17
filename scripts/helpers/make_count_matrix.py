import sys
import csv

build = sys.argv[1]
gtf = sys.argv[2]
method = sys.argv[3]
n_reps = int(sys.argv[4])
depth = sys.argv[5]

folder_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + str(n_reps) + "_" + depth + "/sim/"
gtf_loc = folder_loc + "sim_counts_matrix.csv"
out_loc = folder_loc + method + ".csv"

## get gtf names ##
counts = {}
q = 0
ll = []
with open(gtf_loc, "r") as f:
    lines = f.readlines()
    for x in lines[1:]:
        buff = x.strip().split(",")
        ll += [buff[0]]
        counts[buff[0]] = [0] * 2 * n_reps
## make count matrix ##
for x in range(1, 2*(n_reps) + 1):
    counts_loc = folder_loc + "sample_" + str(x).zfill(2) + "/counts/" + method + ".txt"
    with open(counts_loc, "r") as f:
        lines = f.readlines()
        for y in lines[1:]:
            name,count = y.strip().split(",")
            if name not in counts.keys():
                continue
            counts[name][x-1] += int(count)

header = ["herv"] + ["sample_" + str(x).zfill(2) for x in range(1, 2*(n_reps)+1)]


## tecount mod ##
if method == "tecount":
    counts = {}
    for x in range(1, 2*(n_reps) + 1):
        counts_loc = folder_loc + "sample_" + str(x).zfill(2) + "/counts/" + method + ".txt"
        with open(counts_loc, "r") as f:
            lines = f.readlines()
            for l in lines[1:]:
                buff = l.strip().split(",")
                if buff[0] not in counts.keys():
                    counts[buff[0]] = [buff[1]]
                else:
                    counts[buff[0]] += [buff[1]]
    


## write csv ##
with open(out_loc, "w") as f:
    f.write(",".join(header) + "\n")
    for x in counts.items():
        buff = [x[0]] + x[1]
        f.write(",".join([str(y) for y in buff])+ "\n")
