import pandas as pd

srrs = ["SRR30947472", "SRR30947473", "SRR30947474", "SRR30947477", 
        "SRR30947483", "SRR30947495", "SRR30947506", "SRR30947507"]

methods = ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]


base_loc = "/lustre/research/dawli/stexocaelum/longbench/"
out_loc = "/home/stexocae/data_xfer/longbench_counts.csv"
counts = [["sample", "method", "n_map"]]
for x in srrs:
    for y in methods:
        print(x,y)
        counts_loc = base_loc + x + "/" + y + "/final_counts.csv"
        buff_df = pd.read_csv(counts_loc, index_col=0, header=None)
        buff_df = buff_df[buff_df.loc[:,1] >=2]
        counts += [[x, y, str(int(buff_df.loc[:,1].sum()))]]


with open(out_loc, "w") as f:
    for line in counts:
        f.write(",".join(line) + "\n")
