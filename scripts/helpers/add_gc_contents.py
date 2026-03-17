import sys
import subprocess


method = sys.argv[1]
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/" + method + ".gtf"
genome_loc = "/home/stexocae/li_lab/saem/refs/hs1.fa"
out_loc = "/lustre/work/stexocae/li_lab/" + method + "_gc.out"

bedtools_call = "bedtools getfasta -fi " + genome_loc + " -bed " + gtf_loc + " -fo " + out_loc
#subprocess.run(bedtools_call, shell=True)

gc_contents = {}

def calc_gc(nts):
    gc = round((nts.count('g') + nts.count('G') + nts.count('c') + nts.count('C'))/len(nts), 3)
    return gc

with open(out_loc, "r") as f:
    for line in f.readlines():
        if line[0] == ">":
            name = line[1:].strip()
        else:
            gc = calc_gc(line.strip())
            gc_contents[name] = gc

out_gtf = []
with open(gtf_loc, "r") as f:
    for line in f.readlines():
        buff = line.strip().split()
        name = buff[0] + ":" + str(int(buff[3])-1) + "-" + buff[4]
        out_gtf += [line.strip() + " gc_content \"" + str(gc_contents[name]) + "\";\n"]

with open(gtf_loc, "w") as f:
    for line in out_gtf:
        f.write(line)
