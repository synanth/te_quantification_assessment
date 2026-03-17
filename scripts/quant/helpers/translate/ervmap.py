import sys

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

in_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/ervmap/" + sample + "/herv_coverage_GRCh38_genome.txt"
out_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/" + sample + "/counts/ervmap.txt"
key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/ervmap.txt"
if gtf == "superset" or gtf == "herv" or gtf == "line":
    key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/ervmap_to_superset.txt"
else:
    key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/ervmap_to_" + gtf + ".txt"

translation = {}
with open(key, "r") as f:
    lines = f.readlines()
    for x in lines:
        buff = x.strip().split(',')
        translation[buff[0]] = buff[1]
counts = [["name", "count"]]
unrepresented = 0
with open(in_counts, "r") as f:
    lines = f.readlines()
    for x in lines:
        buff = x.strip().split()
        if buff[3] in translation.keys():
            counts += [[translation[buff[3]], buff[-1]]]
        else:
            unrepresented += int(buff[-1])
print(unrepresented)
counts += [["unrepresented", str(unrepresented)]]

with open(out_counts, "w") as f:
    for x in counts:
        f.write(x[0] + "," + x[1] + "\n")
