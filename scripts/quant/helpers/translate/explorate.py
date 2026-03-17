import sys

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

in_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/explorate/" + sample + "/quant_out/" + sample + "/quant.sf"
out_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/" + sample + "/counts/explorate.txt"
key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/explorate_to_" + gtf + ".txt"


translation = {}
with open(key, "r") as f:
    lines = f.readlines()
    for x in lines:
        buff = x.strip().split(',')
        translation[buff[0]] = buff[1]
counts = [["name", "count"]]
not_counted = 0

unrepresented = 0
with open(in_counts, "r") as f:
    lines = f.readlines()
    for x in lines[1:]:
        buff = x.strip().split()
        if buff[0] in translation.keys():
            counts += [[translation[buff[0]], str(round(float(buff[-1])))]]
        else:
            not_counted +=1
            unrepresented += round(float(buff[-1]))
counts += [["unrepresented", str(unrepresented)]]


with open(out_counts, "w") as f:
    for x in counts:
        f.write(x[0] + "," + x[1] + "\n")
