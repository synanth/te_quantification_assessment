from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

data_loc = "/lustre/research/dawli/stexocaelum/longbench/other_gtf.csv"
viz_loc = "/home/stexocae/data_xfer/other_gtf.png"
convert_name = {"ervmap" : "ERVmap", 
                "te-saem" : "TE-SAEM",
                "telescope" : "Telescope"}
colors = ["#d62800", "#ff9b56", "#d462a6", "#a40062"]
d = []


with open(data_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        d += [line.strip().split(",")]
df = pd.DataFrame(d)
header = df.iloc[0].values
df.columns = header
df = df.drop(index=0, axis=0)
df = df.reset_index(drop=True)
df[["spearman", "pearson", "mae", "rmse"]] = df[["spearman", "pearson", "mae", "rmse"]].apply(pd.to_numeric)
symbols = {"ervmap" : "circle", "telescope" : "square"}
colors = {"ervmap" : "#d70270", "te-saem" : "#a349a4", "telescope" : "#0000ff"}
convert_assess = {"spearman" : "Spearman's", "pearson" : "Pearson's", "mae" : "MAE", "rmse" : "RMSE"}

methods = ["ervmap", "te-saem", "telescope"]
lrs = list(set(df["long_srr"]))

fig = make_subplots(rows=1, cols=4) 
fig.update_layout(font_family="Arial", boxmode='group', showlegend=False, margin=dict(l=20, r=20, t=120, b=20))

for i, assessment in enumerate(["spearman", "pearson", "mae", "rmse"]):
    for g in symbols:
        df_g = df.loc[df["gtf"] == g]
        for m in methods:
            df_m = df_g.loc[df_g["method"] == m]
            fig.add_trace(go.Scatter(mode="markers", y=df_m[assessment], x = df_m["long_srr"], marker=dict(color=colors[m], symbol=symbols[g])), row=1, col=i+1)
    fig.add_annotation(xref = "x domain", yref="y domain", x=0.5, y =1.10, showarrow=False, text=convert_assess[assessment], row=1, col=i+1, font=dict(size=14))


fig.add_annotation(xref = "paper", yref="paper", x=0.5, y =1.5, showarrow=False, text="TE-SAEM's comparative performance when using other GTFs", font=dict(size=18))
fig.add_annotation(xref = "paper", yref="paper", x=0.35, y =1.35, showarrow=False, text="GTF", font=dict(size=16))
fig.add_annotation(xref = "paper", yref="paper", x=0.65, y =1.35, showarrow=False, text="Method", font=dict(size=16))

fig.add_shape(type="circle", xref="paper", yref="paper", x0=0.28, x1=0.29, y0=1.19, y1=1.24, fillcolor="black")
fig.add_annotation(xref = "paper", yref="paper", x=0.295, y =1.26, showarrow=False, text="ERVmap", font=dict(size=14))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.36, x1=0.37, y0=1.19, y1=1.24, fillcolor="black")
fig.add_annotation(xref = "paper", yref="paper", x=0.405, y =1.26, showarrow=False, text="Telescope", font=dict(size=14))


fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.52, x1=0.53, y0=1.19, y1=1.24, fillcolor=colors["ervmap"], line=dict(color=colors["ervmap"]))
fig.add_annotation(xref = "paper", yref="paper", x=0.56, y =1.26, showarrow=False, text="ERVmap", font=dict(size=14))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.6, x1=0.61, y0=1.19, y1=1.24, fillcolor=colors["te-saem"], line=dict(color=colors["te-saem"]))
fig.add_annotation(xref = "paper", yref="paper", x=0.645, y =1.26, showarrow=False, text="TE-SAEM", font=dict(size=14))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.69, x1=0.7, y0=1.19, y1=1.24, fillcolor=colors["telescope"], line=dict(color=colors["telescope"]))
fig.add_annotation(xref = "paper", yref="paper", x=0.765, y =1.26, showarrow=False, text="Telescope", font=dict(size=14))


fig.write_image(height=400, width=1200, file=viz_loc, format="png")
quit()
