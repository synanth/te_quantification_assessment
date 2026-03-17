import sys
import pandas as pd
import math
import subprocess
import numpy as np
import random

#lr = sys.argv[1]
#sr = sys.argv[2]

methods = ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]
base_loc = "/lustre/research/dawli/stexocaelum/longbench/"

lr_to_sr = {"SRR30947491" : "SRR30947472", "SRR30947492" : "SRR30947473",
            "SRR30947493" : "SRR30947477", "SRR30947494" : "SRR30947474",
            "SRR30947496" : "SRR30947483", "SRR30947497" : "SRR30947495", 
            "SRR30947498" : "SRR30947506", "SRR30947499" : "SRR30947507"}

out_csv = [["long_srr", "short_srr", "method", "spearman", "pearson", "mae", "rmse"]]
out_loc = base_loc + "out.csv"

for lr, sr in lr_to_sr.items():
    print(out_csv[0])
    lr_fq_loc = base_loc + lr + "/" + lr + ".fastq"
    sr_fq_loc = base_loc + sr + "/" + sr + "_1.fastq"
    for method in methods:
        lr_counts = {}
        sr_counts = {}
        lrs = []
        srs = []
        tp, fp, fn = 0, 0, 0
        gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/" + method + ".gtf"  
        long_read_loc = base_loc + lr + "/fc_" + method + ".out"
        short_read_loc = base_loc + sr + "/" + method + "/final_counts.csv"

        with open(long_read_loc, "r") as f:
            for line in f.readlines()[2:]:
                buff = line.strip().split()
                if float(buff[-1]) < 2:
                    continue
                lr_counts[buff[0]] = float(buff[-1])
        lr_sum = sum(lr_counts.values())
        lr_counts = {k:v/lr_sum*1e6 for k,v in lr_counts.items()}
        with open(short_read_loc, "r") as f:
            for line in f.readlines():
                buff = line.strip().split(",")
                sr_counts[buff[0]] = float(buff[-1])
        sr_sum = sum(sr_counts.values())
        sr_counts = {k:v/sr_sum*1e6  for k,v in sr_counts.items()}
        with open(gtf_loc, "r") as f:
            for line in f.readlines():
                buff = line.strip().split()
                name = buff[11][1:-2]
                if (lr_counts.get(name, 0) == 0):
                    continue
                lrs += [math.log2(lr_counts.get(name,0)+1)]
                srs += [math.log2(sr_counts.get(name,0)+1)]
         
        df = pd.DataFrame({"lr" : lrs, "sr" : srs})
        spearman = str(df["sr"].corr(df["lr"], method="spearman").item())
        pearson = str(df["sr"].corr(df["lr"], method="pearson").item())
        mae = str(np.mean(np.abs(df["lr"] - df["sr"])).item())
        rmse = str(np.sqrt(np.mean((df["lr"] - df["sr"])**2)).item())
        out_csv += [[lr, sr, method, spearman, pearson, mae, rmse]]
        print(out_csv[-1])

with open(out_loc, "w") as f:
    for line in out_csv:
        f.write(",".join(line) + "\n")
