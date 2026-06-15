import subprocess

srrs = ["SRR8961823", "SRR8961824", "SRR8961825", "SRR8961826", "SRR8961827",
        "SRR8961828", "SRR8961829", "SRR8961830", "SRR8961831", "SRR8961832",
        "SRR8961833", "SRR8961834", "SRR8961835", "SRR8961836", "SRR8961837",
        "SRR8961838", "SRR8961839", "SRR8961840", "SRR8961841", "SRR8961842"]

base_loc = "/lustre/research/dawli/stexocaelum/manu_me_cfs/" 
gtf_loc = "/home/stexocae/li_lab/saem/refs/hs1.gtf"
out_loc = base_loc + "counts.csv"

tes = {}

with open(gtf_loc, "r") as f:
    for line in f.readlines():
        buff = line.strip().split()
        name = buff[11][1:-2]
        tes[name] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for idx, srr in enumerate(srrs):
    data_loc = base_loc + srr + "/te_counts.csv"
    with open(data_loc, "r") as f:
        for line in f.readlines():
            buff = line.strip().split(",")
            tes[buff[0]][idx] = int(buff[1])

with open(out_loc, "w") as f:
    f.write(",".join(srrs) + "\n")
    for k,v in tes.items():
        f.write(k + "," + ",".join([str(x) for x in v]) + "\n")
