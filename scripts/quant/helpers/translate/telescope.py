import sys

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

in_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/telescope/" + sample + "/telescope-telescope_report.tsv"
out_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/" + sample + "/counts/telescope.txt"
key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/telescope.txt"

key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/telescope_to_" + gtf + ".txt"


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
    for x in lines[3:]:
        buff = x.strip().split()
        if buff[0] in translation.keys():
            counts += [[translation[buff[0]], buff[2]]]
        else:
            not_counted += int(buff[2])
print(not_counted)
print(counts[-5:])
print(len(counts))
counts += [["unrepresented", str(not_counted)]]
print(counts[-5:])
with open(out_counts, "w") as f:
    for x in counts:
        f.write(x[0] + "," + x[1] + "\n")
