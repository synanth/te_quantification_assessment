from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from sklearn.decomposition import PCA
from scipy.stats import chi2


colors = ["#fe9ace", "#8ea6ff", "#ff53bf", "#6760fe"]
base_loc = "/home/stexocae/data_xfer/"
viz_loc = base_loc + "applications.png"


## ms ##
ms_loc = base_loc + "ms_degs.csv"
ms_vsd_loc = base_loc + "ms_vsd.csv"
ms_meta_loc = "/lustre/research/dawli/stexocaelum/ms_data/metadata.csv"

df_ms = pd.read_csv(ms_loc, index_col=0)
df_vsd_ms = pd.read_csv(ms_vsd_loc, index_col=0).T
df_ms_meta = pd.read_csv(ms_meta_loc, index_col=0)

tes_for_pca = df_ms.sort_values(by="pvalue")[:10].index.tolist()
df_ms_pca = df_vsd_ms.loc[:,tes_for_pca]
pca = PCA(n_components=2)
ms_pca = pca.fit_transform(df_ms_pca)
ms_pca = pd.DataFrame(data=ms_pca, columns=["pc1", "pc2"], index=df_ms_pca.index)
ms_pca["condition"] = df_ms_meta["condition"]
ms_pc_percent = [str(round(x*100,1)) for x in pca.explained_variance_ratio_]

ms_case = ms_pca[ms_pca["condition"] == "case"]
ms_control = ms_pca[ms_pca["condition"] == "control"]

ms_up = df_ms[(df_ms["padj"] <= .05) & (df_ms["log2FoldChange"] >= 1)]
ms_down = df_ms[(df_ms["padj"] <= .05) & (df_ms["log2FoldChange"] <= -1)]

pval = max(list(ms_up["pvalue"]) + list(ms_down["pvalue"]))
for_cutoff = df_ms.sort_values(by="pvalue")
ms_cutoff = (for_cutoff[for_cutoff["padj"] >= .05][:1]["pvalue"].iloc[0] + pval)/2

ms_pc1_bounds = max(list(abs(ms_pca["pc1"])))
ms_pc1_bounds += .25 * ms_pc1_bounds
ms_pc2_bounds = max(list(abs(ms_pca["pc2"])))
ms_pc2_bounds += .25 * ms_pc2_bounds
ms_l2fc_bounds = max(list(ms_up["log2FoldChange"]) + list(ms_down["log2FoldChange"]))
ms_l2fc_bounds += .25 * ms_l2fc_bounds


## me_cfs ##
me_loc = base_loc + "me_degs.csv"
me_vsd_loc = base_loc + "me_vsd.csv"
me_meta_loc = "/lustre/research/dawli/stexocaelum/manu_me_cfs/metadata.csv"

df_me = pd.read_csv(me_loc, index_col=0)
df_vsd_me = pd.read_csv(me_vsd_loc, index_col=0).T
df_me_meta = pd.read_csv(me_meta_loc, index_col=0)

tes_for_pca = df_me.sort_values(by="padj")[:10].index.tolist()
df_me_pca = df_vsd_me.loc[:,tes_for_pca]
pca = PCA(n_components=2)
me_pca = pca.fit_transform(df_me_pca)
me_pca = pd.DataFrame(data=me_pca, columns=["pc1", "pc2"], index=df_me_pca.index)
me_pca["condition"] = df_me_meta["condition"]
me_pc_percent = [str(round(x*100,1)) for x in pca.explained_variance_ratio_]

me_case = me_pca[me_pca["condition"] == "case"]
me_control = me_pca[me_pca["condition"] == "control"]

me_up = df_me[(df_me["padj"] <= .05) & (df_me["log2FoldChange"] >= 1)]
me_down = df_me[(df_me["padj"] <= .05) & (df_me["log2FoldChange"] <= -1)]

pval = max(list(me_up["pvalue"]) + list(me_down["pvalue"]))
for_cutoff = df_me.sort_values(by="pvalue")
me_cutoff = (for_cutoff[for_cutoff["padj"] >= .05][:1]["pvalue"].iloc[0] + pval)/2

me_pc1_bounds = max(list(abs(me_pca["pc1"])))
me_pc1_bounds += .25 * me_pc1_bounds
me_pc2_bounds = max(list(abs(me_pca["pc2"])))
me_pc2_bounds += .25 * me_pc2_bounds
me_l2fc_bounds = max(list(me_up["log2FoldChange"]) + list(me_down["log2FoldChange"]))
me_l2fc_bounds += .25 * me_l2fc_bounds


## aud ##
aud_loc = base_loc + "aud_degs.csv"
aud_vsd_loc = base_loc + "aud_vsd.csv"
aud_meta_loc = "/lustre/research/dawli/stexocaelum/nac_aud/metadata.csv"

df_aud = pd.read_csv(aud_loc, index_col=0)
df_aud = df_aud[df_aud["pvalue"] < .5]
df_vsd_aud = pd.read_csv(aud_vsd_loc, index_col=0).T
df_aud_meta = pd.read_csv(aud_meta_loc, index_col=0)

tes_for_pca = df_aud.sort_values(by="pvalue")[:10].index.tolist()
df_aud_pca = df_vsd_aud.loc[:,tes_for_pca]
pca = PCA(n_components=2)
aud_pca = pca.fit_transform(df_aud_pca)
aud_pca = pd.DataFrame(data=aud_pca, columns=["pc1", "pc2"], index=df_aud_pca.index)
aud_pca["condition"] = df_aud_meta["condition"]
aud_pc_percent = [str(round(x*100,1)) for x in pca.explained_variance_ratio_]

aud_case = aud_pca[aud_pca["condition"] == "case"]
aud_control = aud_pca[aud_pca["condition"] == "control"]

aud_up = df_aud[(df_aud["padj"] <= .05) & (df_aud["log2FoldChange"] >= 1)]
aud_down = df_aud[(df_aud["padj"] <= .05) & (df_aud["log2FoldChange"] <= -1)]

pval = max(list(aud_up["pvalue"]) + list(aud_down["pvalue"]))
for_cutoff = df_aud.sort_values(by="pvalue")
aud_cutoff = (for_cutoff[for_cutoff["padj"] >= .05][:1]["pvalue"].iloc[0] + pval)/2


aud_pc1_bounds = max(list(abs(aud_pca["pc1"])))
aud_pc1_bounds += .25 * aud_pc1_bounds
aud_pc2_bounds = max(list(abs(aud_pca["pc2"])))
aud_pc2_bounds += .25 * aud_pc2_bounds
aud_l2fc_bounds = max(list(aud_up["log2FoldChange"]) + list(aud_down["log2FoldChange"]))
aud_l2fc_bounds += .25 * aud_l2fc_bounds

## plots ##
fig = make_subplots(rows=3, cols=2,
                    horizontal_spacing = 0.1, vertical_spacing = 0.1)
fig.update_layout(plot_bgcolor="#ffffff", font_family="Arial", showlegend=False, 
                  margin = {"l" :20, "r" : 20, "t" : 100, "b" : 50}) 
fig.update_yaxes(showgrid=False, ticks="inside", showline=True, linewidth=1, linecolor="black", 
                 title_font_size=16, mirror=True)
fig.update_xaxes(showgrid=False, ticks="inside", showline=True, linewidth=1, linecolor="black", 
                 title_font_size=16, mirror=True)


fig.add_trace(go.Scattergl(x=ms_case["pc1"], y=ms_case["pc2"], mode="markers", marker_size=10,
                           marker_color=colors[0]), row=1, col=1)
fig.add_trace(go.Scattergl(x=ms_control["pc1"], y=ms_control["pc2"], mode="markers", marker_size=10,
                           marker_color=colors[1]), row=1, col=1)
fig.update_xaxes(range=[-1 * ms_pc1_bounds, ms_pc1_bounds], title="PC1: " + ms_pc_percent[0] + "%",
                 row=1, col=1)
fig.update_yaxes(range=[-1 * ms_pc2_bounds, ms_pc2_bounds], title="PC2: " + ms_pc_percent[1] + "%",
                 row=1, col=1)

fig.add_trace(go.Scattergl(x=df_ms["log2FoldChange"], y = -1 * np.log10(df_ms["pvalue"]), mode="markers",
                           marker_color="gray", opacity=.1, marker_size=10), row=1, col=2)
fig.add_trace(go.Scattergl(x=ms_up["log2FoldChange"], y = -1 * np.log10(ms_up["pvalue"]), mode="markers",
                           marker_color=colors[2], marker_size=10), row=1, col=2)
fig.add_trace(go.Scattergl(x=ms_down["log2FoldChange"], y = -1 * np.log10(ms_down["pvalue"]), mode="markers",
                           marker_color=colors[3], marker_size=10), row=1, col=2)
fig.add_vline(x=1, line_dash="dash", line_color="#777777", row=1, col=2)
fig.add_vline(x=-1, line_dash="dash", line_color="#777777", row=1, col=2)
fig.add_hline(y=-1*np.log10(ms_cutoff), line_dash="dash", line_color="#777777", row=1, col=2)
fig.update_xaxes(range=[-1 * ms_l2fc_bounds, ms_l2fc_bounds], title="Log2 Fold-Change", row=1, col=2)
fig.update_yaxes(title="-log10( <i>P</i> value )", row=1, col=2)


fig.add_trace(go.Scattergl(x=me_case["pc1"], y=me_case["pc2"], mode="markers", marker_size=10,
                           marker_color=colors[0]), row=2, col=1)
fig.add_trace(go.Scattergl(x=me_control["pc1"], y=me_control["pc2"], mode="markers", marker_size=10,
                           marker_color=colors[1]), row=2, col=1)
fig.update_xaxes(range=[-1 * me_pc1_bounds, me_pc1_bounds], title="PC1: " + me_pc_percent[0] + "%",
                 row=2, col=1)
fig.update_yaxes(range=[-1 * me_pc2_bounds, me_pc2_bounds], title="PC2: " + me_pc_percent[1] + "%",
                 row=2, col=1)

fig.add_trace(go.Scattergl(x=df_me["log2FoldChange"], y = -1 * np.log10(df_me["pvalue"]), mode="markers",
                           marker_color="gray", opacity=.1, marker_size=10), row=2, col=2)
fig.add_trace(go.Scattergl(x=me_up["log2FoldChange"], y = -1 * np.log10(me_up["pvalue"]), mode="markers",
                           marker_color=colors[2], marker_size=10), row=2, col=2)
fig.add_trace(go.Scattergl(x=me_down["log2FoldChange"], y = -1 * np.log10(me_down["pvalue"]), mode="markers",
                           marker_color=colors[3], marker_size=10), row=2, col=2)
fig.add_vline(x=1, line_dash="dash", line_color="#777777", row=2, col=2)
fig.add_vline(x=-1, line_dash="dash", line_color="#777777", row=2, col=2)
fig.add_hline(y=-1*np.log10(me_cutoff), line_dash="dash", line_color="#777777", row=2, col=2)
fig.update_xaxes(range=[-1 * me_l2fc_bounds, me_l2fc_bounds], title="Log2 Fold-Change", row=2, col=2)
fig.update_yaxes(title="-log10( <i>P</i> value )", row=2, col=2)


fig.add_trace(go.Scattergl(x=aud_case["pc1"], y=aud_case["pc2"], mode="markers", marker_size=10,
                           marker_color=colors[0]), row=3, col=1)
fig.add_trace(go.Scattergl(x=aud_control["pc1"], y=aud_control["pc2"], mode="markers", marker_size=10,
                           marker_color=colors[1]), row=3, col=1)
fig.update_xaxes(range=[-1 * aud_pc1_bounds, aud_pc1_bounds], title="PC1: " + aud_pc_percent[0] + "%",
                 row=3, col=1)
fig.update_yaxes(range=[-1 * aud_pc2_bounds, aud_pc2_bounds], title="PC2: " + aud_pc_percent[1] + "%",
                 row=3, col=1)

fig.add_trace(go.Scattergl(x=df_aud["log2FoldChange"], y = -1 * np.log10(df_aud["pvalue"]), mode="markers",
                           marker_color="gray", opacity=.1, marker_size=10), row=3, col=2)
fig.add_trace(go.Scattergl(x=aud_up["log2FoldChange"], y = -1 * np.log10(aud_up["pvalue"]), mode="markers",
                           marker_color=colors[2], marker_size=10), row=3, col=2)
fig.add_trace(go.Scattergl(x=aud_down["log2FoldChange"], y = -1 * np.log10(aud_down["pvalue"]), mode="markers",
                           marker_color=colors[3], marker_size=10), row=3, col=2)
fig.add_vline(x=1, line_dash="dash", line_color="#777777", row=3, col=2)
fig.add_vline(x=-1, line_dash="dash", line_color="#777777", row=3, col=2)
fig.add_hline(y=-1*np.log10(aud_cutoff), line_dash="dash", line_color="#777777", row=3, col=2)
fig.update_xaxes(range=[-1 * aud_l2fc_bounds, aud_l2fc_bounds], title="Log2 Fold-Change", row=3, col=2)
fig.update_yaxes(title="-log10( <i>P</i> value )", row=3, col=2)



## legend ##
locs = [.09, .24, .61, .81]
text_locs = [.11, .26, .73, .95]
fig.add_shape(type="rect", xref="paper", yref="paper", x0=locs[0], x1=locs[0]+.015, y0=1.04, y1=1.055, 
              line_color=colors[0], fillcolor=colors[0])
fig.add_shape(type="rect", xref="paper", yref="paper", x0=locs[1], x1=locs[1]+.015, y0=1.04, y1=1.055, 
              line_color=colors[1], fillcolor=colors[1])
fig.add_shape(type="rect", xref="paper", yref="paper", x0=locs[2], x1=locs[2]+.015, y0=1.04, y1=1.055, 
              line_color=colors[2], fillcolor=colors[2])
fig.add_shape(type="rect", xref="paper", yref="paper", x0=locs[3], x1=locs[3]+.015, y0=1.04, y1=1.055, 
              line_color=colors[3], fillcolor=colors[3])

fig.add_annotation(text="Case", xref="paper", yref="paper", x=text_locs[0], y=1.0575, 
                   font_size= 16, showarrow=False)
fig.add_annotation(text="Control", xref="paper", yref="paper", x=text_locs[1], y=1.0575, 
                   font_size= 16, showarrow=False)
fig.add_annotation(text="Upregulated", xref="paper", yref="paper", x=text_locs[2], y=1.0575, 
                   font_size= 16, showarrow=False)
fig.add_annotation(text="Downregulated", xref="paper", yref="paper", x=text_locs[3], y=1.0575, 
                   font_size= 16, showarrow=False)

fig.add_annotation(text="A", xref="paper", yref="paper", font_size=24, showarrow=False, x=-.05, y=1.03)
fig.add_annotation(text="B", xref="paper", yref="paper", font_size=24, showarrow=False, x=-.05, y=.68) 
fig.add_annotation(text="C", xref="paper", yref="paper", font_size=24, showarrow=False, x=-.05, y=.3) 

fig.add_annotation(text="Multiple Sclerosis", xref="paper", yref="paper", font_size=18, showarrow=False, x=.5, y=1.03)
fig.add_annotation(text="ME/CFS", xref="paper", yref="paper", font_size=18, showarrow=False, x=.5, y=.68) 
fig.add_annotation(text="Alcohol Use Disorder", xref="paper", yref="paper", font_size=18, showarrow=False, x=.5, y=.3) 


width_px = 85*(300/25.4)
height_px = 100*(300/25.4)
fig.write_image(width=width_px, height=height_px, file=viz_loc, format="png")
