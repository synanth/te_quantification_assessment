import sys
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.decomposition import PCA
from scipy.stats import chi2


## data locs ##
base_loc = "/home/stexocae/data_xfer/"
deg_loc = base_loc + "ms_degs.csv"
vsd_loc = base_loc + "ms_vsd.csv"
metadata_loc = "/lustre/research/dawli/stexocaelum/ms_data/metadata.csv"
viz_loc = base_loc + "ms_viz.png"
raw_loc = "/lustre/research/dawli/stexocaelum/ms_data/counts.csv"


## process csv and wrangle data ##
colors = ["#fe9ace", "#ff53bf", "#8ea6ff", "#6760fe", "#200044"]
deg_df = pd.read_csv(deg_loc, index_col=0)
pca_df = pd.read_csv(vsd_loc, index_col=0).T
metadata_df = pd.read_csv(metadata_loc, index_col=0)
raw_df = pd.read_csv(raw_loc, index_col=0)

tes_for_pca = deg_df.sort_values(by="padj")[:100].index.tolist()
pca_df = pca_df.loc[:,tes_for_pca]

pca = PCA(n_components=2)
pca_fit = pca.fit_transform(pca_df)
pca_fit = pd.DataFrame(data = pca_fit, columns = ['pc1', 'pc2'], index=pca_df.index)
pca_fit["condition"] = metadata_df["condition"]
deg_df = deg_df.dropna()

top_tes = deg_df.sort_values(by="padj")[:4]
top_raw = raw_df.loc[top_tes.index]
top_case = top_raw[metadata_df.index[metadata_df["condition"] == "case"].tolist()]
top_control = top_raw[metadata_df.index[metadata_df["condition"] == "control"].tolist()]
te_names = top_tes.index.tolist()



## Make plots ##
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## main layout ##
fig = make_subplots(rows=3, cols=4, 
    subplot_titles=("PCA of top 100 TEs based on adjusted <i>P</i>-value", "Volcano plot", te_names[0], te_names[1], te_names[2], te_names[3]),
    specs = [[{"colspan" : 2, "rowspan" : 2, "r" : 0.025}, None, {"colspan" : 2, "rowspan" : 2, "l" : 0.025}, None],
             [None, None, None, None],
             [{}, {}, {}, {}]],
    horizontal_spacing = 0.02,
    vertical_spacing = 0.1)

fig.update_layout(plot_bgcolor="#ffffff", font_family="Arial", showlegend=False, margin=dict(l=20, r=20, t=60, b=50))


## pca ##
pca_case = pca_fit[pca_fit["condition"] == "case"]
pca_control = pca_fit[pca_fit["condition"] == "control"]
fig.add_trace(go.Scattergl(x=pca_case["pc1"], y = pca_case["pc2"], mode='markers', marker_color=colors[0], marker_size=10), row=1, col=1)
fig.add_trace(go.Scattergl(x=pca_control["pc1"], y = pca_control["pc2"], mode='markers', marker_color=colors[2], marker_size=10), row=1, col=1)

x_axis_bounds = max([abs(x) for x in pca_fit["pc1"]])
x_axis_bounds += .05 * x_axis_bounds
y_axis_bounds = max([abs(x) for x in pca_fit["pc2"]])
y_axis_bounds += .05 * y_axis_bounds
pc_percent = [str(round(x*100,2)) for x in pca.explained_variance_ratio_]
fig.update_xaxes(range=[-1*x_axis_bounds, x_axis_bounds], title="PC1: " + pc_percent[0] + "%", row=1, col=1)
fig.update_yaxes(range=[-1*y_axis_bounds, y_axis_bounds], title="PC2: " + pc_percent[1] + "%", row=1, col=1)


## pca ellipse from AI prompt ##
def get_ellipse_coords(data, confidence=0.68):
    # Calculate mean and covariance
    mu = np.mean(data, axis=0)
    cov = np.cov(data, rowvar=False)

    # Eigen decomposition for axes and rotation
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]

    # Scale axes by confidence interval
    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    width, height = 2 * np.sqrt(vals * chi2.ppf(confidence, df=2))

    # Generate points
    t = np.linspace(0, 2*np.pi, 100)
    ell = np.array([np.cos(t) * width/2, np.sin(t) * height/2])
    R = np.array([[np.cos(np.radians(theta)), -np.sin(np.radians(theta))],
                  [np.sin(np.radians(theta)), np.cos(np.radians(theta))]])

    return (R @ ell).T + mu
#print(pca_case.drop(columns=['condition']).values)
#quit()
ellipse_case = get_ellipse_coords(pca_case.drop(columns=['condition']).values)
fig.add_trace(go.Scatter(x=ellipse_case[:, 0], y=ellipse_case[:, 1], mode='lines', line=dict(dash='dash', color=colors[0])), row=1, col=1)

ellipse_control = get_ellipse_coords(pca_control.drop(columns=['condition']).values)
fig.add_trace(go.Scatter(x=ellipse_control[:, 0], y=ellipse_control[:, 1], mode='lines', line=dict(dash='dash', color=colors[2])), row=1, col=1)

fig.add_annotation(text="A", xref="paper", yref="paper", x=-.05, y=1.05, showarrow=False, font=dict(size=30))


## volcano ##
degs_up = deg_df[(deg_df["padj"] <= .05) & (deg_df["log2FoldChange"] >= 1)]
degs_down = deg_df[(deg_df["padj"] <= .05) & (deg_df["log2FoldChange"] <= -1)]
non_degs = deg_df[(deg_df["padj"] > .05) & (deg_df["log2FoldChange"] < 1) & (deg_df["log2FoldChange"] > -1)]
fig.add_trace(go.Scattergl(x=deg_df["log2FoldChange"], y = -1 * np.log10(deg_df["pvalue"]), mode='markers', marker_color="gray", opacity=0.3, marker_size=10), row=1, col=3)
fig.add_trace(go.Scattergl(x=degs_down["log2FoldChange"], y = -1 * np.log10(degs_down["pvalue"]), mode='markers', marker_color=colors[3], marker_size=10), row=1, col=3)
fig.add_trace(go.Scattergl(x=degs_up["log2FoldChange"], y = -1 * np.log10(degs_up["pvalue"]), mode='markers', marker_color=colors[1], marker_size=10), row=1, col=3)
fig.add_vline(x=1, line_dash="dash", line_color="#777777", row=1, col=3)
fig.add_vline(x=-1, line_dash="dash", line_color="#777777", row=1, col=3)
fig.add_hline(y=np.log10(2.6e-6)*-1, line_dash="dash", line_color="#777777", row=1, col=3)

x_axis_bounds = max([abs(x) for x in deg_df["log2FoldChange"]])
x_axis_bounds += .05 * x_axis_bounds
fig.update_xaxes(range=[-1*x_axis_bounds, x_axis_bounds], title="Log2 Fold Change", row=1, col=3)
y_axis_bounds = min([abs(x) for x in deg_df["pvalue"]])
y_axis_bounds -= .5 * y_axis_bounds
fig.update_yaxes(range=[-.5, -1*np.log10(y_axis_bounds)], title="-Log10 (<i>P</i>-value)",row=1, col=3)

fig.add_annotation(text="B", xref="paper", yref="paper", x=.5, y=1.05, showarrow=False, font=dict(size=30))


## counts ##
top_tes = deg_df.sort_values(by="padj")[:4]
top_raw = raw_df.loc[top_tes.index]
top_case = top_raw[metadata_df.index[metadata_df["condition"] == "case"].tolist()]
top_control = top_raw[metadata_df.index[metadata_df["condition"] == "control"].tolist()]
for i in range(0,4):
    viz_case = top_case.iloc[i]
    viz_control = top_control.iloc[i]
    fig.add_trace(go.Box(y=viz_case, jitter=0.5, boxpoints="all", marker={"color" : colors[0]}, name="MS"), row=3, col=i+1)
    fig.add_trace(go.Box(y=viz_control, jitter=0.5, boxpoints="all", marker={"color" : colors[2]}, name="Control"), row=3, col=i+1)
fig.update_yaxes(title="Raw Counts", row=3, col=1)

fig.add_annotation(text="C", xref="paper", yref="paper", x=-.05, y=.275, showarrow=False, font=dict(size=30))



## legend ##
fig.add_shape(type="rect", xref="paper", yref="paper", x0=.13, x1=.14, y0=1.045, y1=1.06, line=dict(color=colors[0]), fillcolor=colors[0])
fig.add_shape(type="rect", xref="paper", yref="paper", x0=.28, x1=.29, y0=1.045, y1=1.06, line=dict(color=colors[2]), fillcolor=colors[2])
fig.add_shape(type="rect", xref="paper", yref="paper", x0=.63, x1=.64, y0=1.045, y1=1.06, line=dict(color=colors[1]), fillcolor=colors[1])
fig.add_shape(type="rect", xref="paper", yref="paper", x0=.84, x1=.85, y0=1.045, y1=1.06, line=dict(color=colors[3]), fillcolor=colors[3])
fig.add_annotation(text="Multiple Sclerosis", xref="paper", yref="paper", x=.141, y= 1.065, showarrow=False, font=dict(size=14))
fig.add_annotation(text="Control", xref="paper", yref="paper", x=.29, y= 1.065, showarrow=False, font=dict(size=14))
fig.add_annotation(text="Upregulated", xref="paper", yref="paper", x=.721, y= 1.065, showarrow=False, font=dict(size=14))
fig.add_annotation(text="Downregulated", xref="paper", yref="paper", x=.95, y= 1.065, showarrow=False, font=dict(size=14))


fig.update_yaxes(showgrid=False, ticks="inside", showline=True, linewidth=1, linecolor="black", mirror=True)
fig.update_xaxes(showgrid=False, ticks="inside", showline=True, linewidth=1, linecolor="black", mirror=True)

fig.write_image(height=900, width=1200, file=viz_loc, format="png")
