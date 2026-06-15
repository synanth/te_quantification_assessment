import subprocess

srrs = ["SRR10248405", "SRR10248406", "SRR10248407", "SRR10248408", "SRR10248439",
        "SRR10248404", "SRR10248411", "SRR10248419", "SRR10248421", "SRR10248427"]

base_loc = "/lustre/research/dawli/stexocaelum/ms_data/" 
gtf_loc = "/home/stexocae/li_lab/saem/refs/hs1.gtf"
out_loc = base_loc + "counts.csv"

tes = {}

with open(gtf_loc, "r") as f:
    for line in f.readlines():
        buff = line.strip().split()
        name = buff[11][1:-2]
        tes[name] = [0,0,0,0,0,0,0,0,0,0]

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
