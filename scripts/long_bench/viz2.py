from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

data_loc = "/lustre/research/dawli/stexocaelum/longbench/other_gtf.csv"
viz_loc = "/home/stexocae/data_xfer/longbench_other.png"
convert_name = {"ervmap" : "ERVmap", 
                "te-saem" : "<b>QuantiTE</b>",
                "telescope" : "Telescope"}
colors = ["#d62800", "#ff9b56", "#d462a6", "#a40062"]
assessments = ["Pearson's", "Spearman's", "MAE", "RMSE"]
d_other = []

with open(data_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        d_other += [line.strip().split(",")]
df_other = pd.DataFrame(d_other)
header = df_other.iloc[0].values
df_other.columns = header
df_other = df_other.drop(index=0, axis=0)
df_other = df_other.reset_index(drop=True)
df_other[["spearman", "pearson", "mae", "rmse"]] = df_other[["spearman", "pearson", "mae", "rmse"]].apply(pd.to_numeric)



## make figures ##
fig = make_subplots(rows=2, cols=2) 
fig.update_layout(font_family="Arial", boxmode="group", showlegend=False, margin=dict(l=20, r=20, t=80, b=20), boxgap=.1, boxgroupgap=0)
colors = ["#d62800", "#ff9b56", "#d462a6", "#a40062"]


df_gtf = df_other[df_other["gtf"] == "ervmap"]
for y in ["ervmap", "te-saem"]:
    df_sub = df_gtf[df_gtf["method"] == y]
    fig.add_trace(go.Box(y=df_sub["pearson"], name=convert_name[y], marker_color=colors[0], offsetgroup="A"), row=1, col=1)
    fig.add_trace(go.Box(y=df_sub["spearman"], name=convert_name[y], marker_color=colors[1], offsetgroup="B"), row=1, col=1)

for y in ["ervmap", "te-saem"]:
    df_sub = df_gtf[df_gtf["method"] == y]
    fig.add_trace(go.Box(y=df_sub["mae"], name=convert_name[y], marker_color=colors[2], offsetgroup="A"), row=1, col=2)
    fig.add_trace(go.Box(y=df_sub["rmse"], name=convert_name[y], marker_color=colors[3], offsetgroup="B"), row=1, col=2)

df_gtf = df_other[df_other["gtf"] == "telescope"]
for y in ["te-saem", "telescope"]:
    df_sub = df_gtf[df_gtf["method"] == y]
    fig.add_trace(go.Box(y=df_sub["pearson"], name=convert_name[y], marker_color=colors[0], offsetgroup="A"), row=2, col=1)
    fig.add_trace(go.Box(y=df_sub["spearman"], name=convert_name[y], marker_color=colors[1], offsetgroup="B"), row=2, col=1)

for y in ["te-saem", "telescope"]:
    df_sub = df_gtf[df_gtf["method"] == y]
    fig.add_trace(go.Box(y=df_sub["mae"], name=convert_name[y], marker_color=colors[2], offsetgroup="A"), row=2, col=2)
    fig.add_trace(go.Box(y=df_sub["rmse"], name=convert_name[y], marker_color=colors[3], offsetgroup="B"), row=2, col=2)


## legend ##
fig.add_annotation(xref="paper", yref="paper", text="A", font_size=20, showarrow=False, x=-.05,y=1.05)
fig.add_annotation(xref="paper", yref="paper", text="B", font_size=20, showarrow=False, x=-.05,y=.45)

name_locs = [.03, .31, .62, .95]

for e,i in enumerate(assessments):
    fig.add_shape(type="rect", xref="paper", yref="paper", x0=.28*e, x1=.28*e+.02, y0=1.05, y1=1.07, fillcolor=colors[e], line_color=colors[e])    
    fig.add_annotation(xref="paper", yref="paper", y=1.08, x=name_locs[e], text=i, showarrow=False, font_size=14)

fig.write_image(height=600, width=600, file=viz_loc, format="png")
