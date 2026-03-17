import csv
import subprocess
from pyliftover import LiftOver

ref_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/"
rm_loc = ref_loc + "bed/ervmap.bed"
chm13_bed_loc = ref_loc +"bed/ervmap_chm13.bed"
gtf_loc = ref_loc + "bed/ervmap.gtf"
out_loc = ref_loc + "simulation/ervmap.gtf"

lo = LiftOver("/lustre/work/stexocae/li_lab/refs/te_annotations/chain/grch38-chm13v2.chain")

out = []

## liftover to chm13 ##
def get_key(s):
    s = s[3:]
    if s.isdigit():
        return int(s)
    elif s == "X":
        return 30
    elif s == "Y":
        return  40
    elif s == "M":
        return 50

with open(rm_loc, "r") as f:
    lines = f.readlines()
    for x in lines:
        buff = x.strip().split()
        if not lo.convert_coordinate(buff[0], int(buff[1]), buff[-1]) or not lo.convert_coordinate(buff[0], int(buff[2]), buff[-1]):
            continue
        buff[1] = lo.convert_coordinate(buff[0], int(buff[1]), buff[-1])[0][1]
        buff[2] = lo.convert_coordinate(buff[0], int(buff[2]), buff[-1])[0][1]
        if buff[1] >= buff[2]:
            continue
        out += [buff]
out.sort(key=lambda x: (get_key(x[0]), x[1]))


with open(chm13_bed_loc, "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(out)

## convert to gtf ##
convert_call = "bedToGenePred " + chm13_bed_loc + " /dev/stdout | genePredToGtf file /dev/stdin " + gtf_loc
subprocess.run(convert_call, shell=True)


## reduce to only whole transcripts 
d = {}
with open(gtf_loc, "r") as f:
    lines = f.readlines()
    for l in lines:
        buff = l.strip().split()
        name = buff[9][1:-2]
        if name not in d:
            d[name] = l

with open(out_loc, "w") as f:
    for x in list(d.values()):
        f.write(x)
   

## clean up ##
#clean_call = "rm -rf " + chm13_bed_loc + " && rm -rf " + gtf_loc
#subprocess.run(clean_call, shell=True)
