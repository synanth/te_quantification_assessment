import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

in_folder = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/texp/" + sample + "/" 
in_counts = in_folder + sample + ".re.filtered.bed"
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/" + gtf + ".gtf"
out_counts = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/" + sample + "/counts/texp.txt"
buff_loc = in_folder + "buff"


orig_counts = {}
with open(in_counts, "r") as f:
    lines = f.readlines()
    for l in lines:
        l = l.split()
        name = l[3]
        if name not in orig_counts.keys():
            orig_counts[name] = 1
        else:
            orig_counts[name] += 1

if gtf == "superset" or gtf == "herv" or gtf == "texp":
    key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/texp_to_superset.txt"
else:
    key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/texp_to_" + gtf + ".txt"
bedtools_call = "bedtools intersect -wo -a " + in_counts + " -b " + gtf_loc + " -f 0.25 -r > " + buff_loc
subprocess.call(bedtools_call, shell=True)

counts = [["name", "count"]]
new_counts = {}
translation = []

with open(buff_loc, "r") as f:
    b_lines = f.readlines()
    for l in b_lines:
        l = l.strip().split()
        orig_name = l[3]
        new_name = l[28][1:-2]
        score = -1*int(l[-1])
        translation += [[orig_name, new_name, score]]
translation = sorted(translation, key=lambda x:(x[0], x[-1]))

seen_names = set()
for x in translation:
    if x[0] in seen_names:
        continue
    else:
        seen_names.add(x[0])
        if x[1] not in new_counts.keys():
            new_counts[x[1]] = 1
        else:
            new_counts[x[1]] += 1

counts += [[key,value] for key, value in new_counts.items()]
val = sum([x[1] for x in counts[1:]])
unrepresented = len(list(orig_counts.keys())) - val

if unrepresented <= 0:
    unrepresented = 0

counts += [["unrepresented", unrepresented]]
with open(out_counts, "w") as f:
    for x in counts:
        f.write(x[0] + "," + str(x[1]) + "\n")
