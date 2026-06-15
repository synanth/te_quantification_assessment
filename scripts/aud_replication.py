from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


base_loc = "/home/stexocae/data_xfer/"
aud1_loc = base_loc + "aud_degs.csv"
aud2_loc = base_loc + "aud2_degs.csv"
lustre_loc = "/lustre/research/dawli/stexocaelum/"
counts1_loc = lustre_loc + "nac_aud/counts.csv"
counts2_loc = lustre_loc + "aud_Backup/counts.csv"
meta1_loc = lustre_loc + "nac_aud/metadata.csv"
meta2_loc = lustre_loc + "aud_Backup/metadata.csv"

aud1_df = pd.read_csv(aud1_loc, index_col=0)
aud2_df = pd.read_csv(aud2_loc, index_col=0)
counts1_df = pd.read_csv(counts1_loc)
counts2_df = pd.read_csv(counts2_loc)
meta1_df = pd.read_csv(meta1_loc)
meta2_df = pd.read_csv(meta2_loc)

viz_loc = base_loc + "top_aud.png"

## data wrangle ##

top_pval1 = aud1_df.sort_values(by="pvalue")[:100].rename(columns={"log2FoldChange" : "l2fc"}).drop(columns=["baseMean", "lfcSE", "stat", "padj"])
top_l2fc1 = aud1_df.sort_values(by="log2FoldChange", key=abs, ascending=False)[:100].rename(columns={"log2FoldChange" : "l2fc"}).drop(columns=["baseMean", "lfcSE", "stat", "padj"])

top_pval2 = aud2_df[aud2_df.index.isin(list(top_pval1.index))].rename(columns={"log2FoldChange" : "l2fc2", "pvalue" : "pvalue2"}).drop(columns=["baseMean", "lfcSE", "stat", "padj"])
top_l2fc2 = aud2_df[aud2_df.index.isin(list(top_l2fc1.index))].rename(columns={"log2FoldChange" : "l2fc2", "pvalue" : "pvalue2"}).drop(columns=["baseMean", "lfcSE", "stat", "padj"])

top_pval = pd.merge(top_pval1, top_pval2, left_index=True, right_index=True)
top_l2fc = pd.merge(top_l2fc1, top_l2fc2, left_index=True, right_index=True)

out_pval = base_loc + "aud_top_pval.csv"
out_l2fc = base_loc + "aud_top_l2fc.csv"

top_pval.to_csv(out_pval)
top_l2fc.to_csv(out_l2fc)

top_pval = top_pval.loc[top_pval["pvalue2"] <= .05].sort_values(by="pvalue2")
top_idx = list(top_pval.index)

counts1_df = counts1_df.loc[top_idx].T.join(meta1_df[["condition"]])
counts2_df = counts2_df.loc[top_idx].T.join(meta2_df[["condition"]])

## plots ##
colors = ["#fe9ace", "#8ea6ff"]

fig = make_subplots(rows=1, cols=5, subplot_titles=top_idx)
fig.update_layout(font_family="Arial", showlegend=False, 
                  margin={"l" : 20, "r" : 20, "b" : 20, "t" : 80})

cases1 = counts1_df.loc[counts1_df["condition"] == "case"]
cases2 = counts2_df.loc[counts2_df["condition"] == "case"]
controls1 = counts1_df.loc[counts1_df["condition"] == "control"]
controls2 = counts2_df.loc[counts2_df["condition"] == "control"]

for e,x in enumerate(top_idx):
    fig.add_trace(go.Box(y=cases1.loc[:,x], jitter=0.5, boxpoints="all", marker={"color" : colors[0]}), row=1,col=e+1)
    fig.add_trace(go.Box(y=cases2.loc[:,x], jitter=0.5, boxpoints="all", marker={"color" : colors[0]}), row=1,col=e+1)
    fig.add_trace(go.Box(y=controls1.loc[:,x], jitter=0.5, boxpoints="all", marker={"color" : colors[1]}), row=1,col=e+1)
    fig.add_trace(go.Box(y=controls2.loc[:,x], jitter=0.5, boxpoints="all", marker={"color" : colors[1]}), row=1,col=e+1)



fig.write_image(height=300, width=1000, file=viz_loc, format="png")
