import subprocess

srrs = ["SRR27494670", "SRR27494681", "SRR27494683", "SRR27494684", "SRR27494686", 
       "SRR27494690", "SRR27494691", "SRR27494692", "SRR27494708", "SRR27494729", 
       "SRR27494740", "SRR27494746", "SRR27494758", "SRR27494783", "SRR27494794", 
       "SRR27494805", "SRR27494813", "SRR27494824", "SRR27494858", "SRR27494859"]

base_loc = "/lustre/research/dawli/stexocaelum/nac_aud/" 
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
