from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

data_loc = "/lustre/research/dawli/stexocaelum/longbench/out.csv"
viz_loc = "/home/stexocae/data_xfer/longbench.png"
convert_name = {"ervmap" : "ERVmap", 
                "explorate" : "ExplorATE",
                "lions" : "LIONS",
                "squire" : "SQuIRE",
                "te-saem" : "TE-SAEM",
                "telescope" : "Telescope",
                "telocal" : "TElocal",
                "tetools" : "TEtools",
                "texp" : "TeXP"}
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
lrs = list(set(df["long_srr"]))

fig = make_subplots(rows=5, cols=4, row_heights = [.245, .245, .02, .245, .245], vertical_spacing=.08, horizontal_spacing = 0.025) 
fig.update_layout(font_family="Arial", boxmode='group', showlegend=False, margin=dict(l=20, r=20, t=120, b=20))
for i, lr in enumerate(lrs):
    df_lr = df.loc[df["long_srr"] == lr].reset_index(drop=True)
    fig.add_trace(go.Scatter(y=df_lr["pearson"], x = [convert_name[x] for x in df_lr["method"]], line=dict(color=colors[0])), row=int(i/4)+1, col=i%4+1)
    fig.add_trace(go.Scatter(y=df_lr["spearman"], x = [convert_name[x] for x in df_lr["method"]], line=dict(color=colors[3])), row=int(i/4)+1, col=i%4+1)
    fig.add_trace(go.Scatter(y=df_lr["mae"], x = [convert_name[x] for x in df_lr["method"]], line=dict(color=colors[1])), row=int(i/4)+4, col=i%4+1)
    fig.add_trace(go.Scatter(y=df_lr["rmse"], x = [convert_name[x] for x in df_lr["method"]], line=dict(color=colors[2])), row=int(i/4)+4, col=i%4+1)

    fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.15, showarrow=False, text=lr, row=int(i/4)+1, col=i%4+1, font=dict(size=14))
    fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.15, showarrow=False, text=lr, row=int(i/4)+4, col=i%4+1, font=dict(size=14))

    fig.update_yaxes(range=[-0.25,1], row=int(i/4)+1, col=i%4+1)
    fig.update_yaxes(range=[0, 6.5], row=int(i/4)+4, col=i%4+1)
fig.update_xaxes(tickangle=45)

## annotations ##
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=1.11, showarrow=False, text="Methods' performances based on correlations with long read data", font=dict(size=18))
fig.add_shape(type="rect", xref="paper", yref="paper", x0=.4, x1=.415, y0=1.05, y1=1.065, line=dict(color=colors[0], width=2), fillcolor=colors[0])
fig.add_annotation(xref="paper", yref="paper", x=.45, y = 1.067, showarrow=False, text="Pearson's", font=dict(size=16))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.52, x1=.535, y0=1.05, y1=1.065, line=dict(color=colors[3], width=2), fillcolor=colors[3])
fig.add_annotation(xref="paper", yref="paper", x=.58, y = 1.067, showarrow=False, text="Spearman's", font=dict(size=16))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.4, x1=.415, y0=.47, y1=.485, line=dict(color=colors[1], width=2), fillcolor=colors[1])
fig.add_annotation(xref="paper", yref="paper", x=.44, y = .476, showarrow=False, text="MAE", font=dict(size=16))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.52, x1=.535, y0=.47, y1=.485, line=dict(color=colors[2], width=2), fillcolor=colors[2])
fig.add_annotation(xref="paper", yref="paper", x=.56, y = .476, showarrow=False, text="RMSE", font=dict(size=16))



fig.write_image(height=1200, width=1200, file=viz_loc, format="png")
