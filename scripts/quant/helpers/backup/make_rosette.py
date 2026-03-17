import csv

ref_loc = "/lustre/work/stexocae/li_lab/refs/"
rm_loc = ref_loc + "hg38/raw/hg38_all.bed"
rosette_loc = ref_loc +"te_annotations/tetools/hg38.txt"

rosette = []
with open(rm_loc, "r") as f:
    lines = f.readlines()
    for x in lines:
        buff= x.strip().split()
        rosette += [buff[3] + "\t" + buff[3] +  "\n"]
with open(rosette_loc, "w") as f:
    for l in rosette:
        f.write(l)
