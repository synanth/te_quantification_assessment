import subprocess

srrs = ["SRR23867362", "SRR23867397", "SRR23867398", "SRR23867399", "SRR23867400",
        "SRR23867426", #"SRR23867427", 
        "SRR23867431", "SRR23867432", "SRR23867425",
        "SRR23867479", "SRR23867480", "SRR23867484", "SRR23867485", "SRR23867486",
        "SRR23867302", "SRR23867303", "SRR23867304", "SRR23867315", "SRR23867389"]

base_loc = "/lustre/research/dawli/stexocaelum/me_cfs2/" 
gtf_loc = "/home/stexocae/li_lab/saem/refs/hs1.gtf"
out_loc = base_loc + "counts.csv"

tes = {}

with open(gtf_loc, "r") as f:
    for line in f.readlines():
        buff = line.strip().split()
        name = buff[11][1:-2]
        #tes[name] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        tes[name] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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
