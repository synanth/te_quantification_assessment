import subprocess

srrs = ["SRR27494667", "SRR27494668", "SRR27494669", "SRR27494671", "SRR27494672",
        "SRR27494673", "SRR27494674", "SRR27494676", "SRR27494719", "SRR27494720",
        "SRR27494666", "SRR27494675", "SRR27494677", "SRR27494678", "SRR27494679",
        "SRR27494680", "SRR27494682", "SRR27494685", "SRR27494687", "SRR27494688"]

base_loc = "/lustre/research/dawli/stexocaelum/aud2/" 
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
