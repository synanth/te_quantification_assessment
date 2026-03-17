import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]

base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/"
in_counts = base_loc + "squire/" + sample + "/quant/" + sample + "_TEcounts.txt"
out_counts = base_loc + "sim/" + sample + "/counts/squire.txt"
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/squire.gtf"
bed_loc = base_loc + "squire/" + sample + "bed"

key = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/translations/" + build + "/squire_to_" + gtf + ".txt"


## convert to bed ##
bed = []
orig_counts = 0
with open(in_counts, "r") as f:
    lines = f.readlines()[1:]
    for x in lines:
        buff = x.strip().split()
        bed += ["\t".join(buff[:4] + [buff[-4]])]
        orig_counts += int(buff[-4])

with open(bed_loc, "w") as f:
    for b in bed:
        f.write(b +"\n")



buff_loc = base_loc + "squire/" +  sample + "buff"
bedtools_call = "bedtools intersect -wo -a " + bed_loc + " -b " + gtf_loc + " -f 0.25 -r > " + buff_loc
subprocess.call(bedtools_call, shell=True)

translation = []
with open(buff_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        old_name = buff[3]
        new_name = buff[16][1:-2]
        count = buff[4]
        score = -1*int(buff[-1])
        translation += [[old_name, new_name, count, score]]
seen_names = set()
translation = sorted(translation, key=lambda x:(x[0], x[-1]))
out = ["name,count"]
n_counts = 0


convert = {}
with open(key, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split(",")
        convert[buff[0]] = buff[1]

for x in translation:
    if x[0] in seen_names:
        continue
    else:
        seen_names.add(x[0])
        if x[1] not in convert.keys():
            continue
        out += [",".join([convert[x[1]], x[2]])]
        n_counts += int(x[2])
unrepresented = orig_counts - n_counts
out += [",".join(["unrepresented", str(unrepresented)])]


with open(out_counts, "w") as f:
    for x in out:
        f.write(x + "\n")
