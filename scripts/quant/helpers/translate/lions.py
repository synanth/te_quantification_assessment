import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

in_folder = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/"
in_counts = in_folder + "lions/" + sample + "/" + sample + "_1.lcsv"
out_counts = in_folder + "sim/" + sample + "/counts/lions.txt"
bed_loc = in_folder + "lions/" + sample + "/" + sample + ".bed"
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/" + gtf + ".gtf"
buff_loc = in_folder + "lions/" + sample + "/buff"

## convert to bed ##
bed = []
orig_counts = {}

with open(in_counts, "r") as f:
    lines = f.readlines()[1:]
    for l in lines:
        l = l.split()
        name = l[2]
        chrom = l[3].split(':')[0]
        start = l[3].split(':')[1].split('-')[0]
        end = l[3].split(':')[1].split('-')[1]
        name = chrom + ":" + start + ":" + end + ":" + name.replace(":", "-")
        count = str(round(float(l[30])))
        bed += [[chrom, start, end, name]]
        if name not in orig_counts.keys():
            orig_counts[name] = int(count)
        else:
            orig_counts[name] += int(count)
with open(bed_loc, "w") as f:
    for x in bed:
        f.write("\t".join(x) + "\n")


## find conversion ##
bedtools_call = "bedtools intersect -wo -a " + bed_loc + " -b " + gtf_loc + " -f 0.25 -r > " + buff_loc

subprocess.call(bedtools_call, shell=True)
counts = [["name", "count"]]
new_counts = {}
not_counted = 0

seen_names = set()
translation = []
with open(buff_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        orig_name = buff[3]
        new_name = buff[15][1:-2]
        score = -1*int(buff[-1])
        translation += [[orig_name, new_name, score]]
translation = sorted(translation, key=lambda x:(x[0], x[-1]))

out = [["name","count"]]
n_counts = 0
for x in translation:
    if x[0] in seen_names:
        continue
    else:
        seen_names.add(x[0])
        out += [[x[1], orig_counts[x[0]]]]
        n_counts += orig_counts[x[0]]
unrepresented = sum(list(orig_counts.values())) - n_counts


## FIX ME ##
out += [["unrepresented", unrepresented]]
with open(out_counts, "w") as f:
    for x in out:
        f.write(x[0] + "," + str(x[1]) + "\n")
