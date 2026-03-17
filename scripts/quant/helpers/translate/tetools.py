import sys

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

in_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/tetools/" + sample 
out_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/" + sample + "/counts/tetools.txt"
key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/tetools.txt"
if gtf == "superset" or gtf == "herv" or gtf == "line":
    key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/tetools_to_superset.txt"
else:
    key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/tetools_to_" + gtf + ".txt"


translation = {}
with open(key, "r") as f:
    lines = f.readlines()
    for x in lines:
        buff = x.strip().split(',')
        translation[buff[0]] = buff[1]
counts = [["name", "count"]]
not_counted = 0
with open(in_counts, "r") as f:
    lines = f.readlines()
    for x in lines:
        buff = x.strip().split()
        if buff[0] in translation.keys():
            counts += [[translation[buff[0]], buff[-1]]]
        else:
            not_counted += int(buff[-1])
counts += [["unrepresented", str(not_counted)]]
with open(out_counts, "w") as f:
    for x in counts:
        f.write(x[0] + "," + x[1] + "\n")
