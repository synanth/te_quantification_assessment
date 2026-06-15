import pandas as pd
import inmoose.pycombat.pycombat_seq as bec

base_loc = "/lustre/research/dawli/stexocaelum/"
aud_loc = base_loc + "nac_aud/counts.csv"
aud2_loc = base_loc + "aud2/counts.csv"
meta_loc = base_loc + "nac_aud/metadata.csv"
meta2_loc = base_loc + "aud2/metadata.csv"
out_loc = "/home/stexocae/data_xfer/batch_aud.csv"

df1 = pd.read_csv(aud_loc, index_col=0).T
df2 = pd.read_csv(aud2_loc, index_col=0).T
metadata1 = pd.read_csv(meta_loc, index_col=0).reindex(df1.index)
metadata2 = pd.read_csv(meta2_loc, index_col=0).reindex(df2.index)

d = pd.concat([df1, df2], axis=0).T
print(d)
b = pd.Series([1]*20+ [2]*20).T
m = pd.concat([metadata1, metadata2], axis=0)

out = bec(d,batch=b, covar_mod=m)
print(type(out))
out_df = pd.DataFrame(out)
out_df.to_csv(out_loc)
