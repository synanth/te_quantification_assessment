import sys

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

in_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/telocal/" + sample + ".cntTable"
out_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/" + sample + "/counts/telocal.txt"
if gtf == "superset" or gtf == "herv" or gtf == "line":
    key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/telocal_to_superset.txt"
else:
    key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/"+ build + "/telocal_to_" + gtf + ".txt"


translation = {}
with open(key, "r") as f:
    lines = f.readlines()
    for x in lines:
        buff = x.strip().split(',')
        translation[buff[0]] = buff[1]
counts = [["name", "count"]]
d = {}
not_counted = 0

with open(in_counts, "r") as f:
    lines = f.readlines()
    for x in lines[1:]:
        buff = x.strip().split()
        name = buff[0].split(":")[0]
        if name in translation.keys():
            if translation[name] not in d.keys():
                d[translation[name]] = int(buff[-1])
            else:
                d[translation[name]] += int(buff[-1])
        else:
            not_counted += int(buff[-1])
res = list(map(lambda item: [item[0], item[1]], d.items()))
counts += res
counts += [["unrepresented", not_counted]]

with open(out_counts, "w") as f:
    for x in counts:
        f.write(x[0] + "," + str(x[1]) + "\n")
