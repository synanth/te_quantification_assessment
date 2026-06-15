import sys
import pandas as pd

## data locs ##
base_loc = "/home/stexocae/data_xfer/"
gtf_loc = "/home/stexocae/li_lab/saem/refs/hs1.gtf"
deg_loc = base_loc + "aud_degs.csv"
out_loc = base_loc + "top_aud.csv"

## process csv and wrangle data ##
deg_df = pd.read_csv(deg_loc, index_col=0)
deg_df = deg_df[deg_df["pvalue"] <= .01]
deg_df = deg_df.sort_values("pvalue")
deg_df["location"] = ["0"]*deg_df.index.size
deg_df["family"] = ["0"]*deg_df.index.size


with open(gtf_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        name = buff[19][1:-2]
        if name in deg_df.index: 
            loc = buff[0] + ":" + buff[3] + "-" + buff[4]
            fam = buff[15][1:-2] + ":" + buff[17][1:-2]
            deg_df.loc[name, "location"] = loc
            deg_df.loc[name, "family"] = fam

print(deg_df)
deg_df.to_csv(out_loc)
