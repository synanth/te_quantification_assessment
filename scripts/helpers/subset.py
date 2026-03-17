import sys

subset_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/hg38_telescope_3_2/sim/subset.gtf"
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/hg38/telescope.gtf"

names = set()
with open(subset_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        names.add(buff[11])

out = []
with open(gtf_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        if buff[11] in names:
            out += [line]


with open(subset_loc, "w") as f:
    for line in out:
        f.write(line)
