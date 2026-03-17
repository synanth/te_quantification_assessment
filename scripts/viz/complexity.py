from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import sys

csv_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/all.csv"
out_loc = "/home/stexocae/data_xfer/complexity.png"


## load csv and wrangle data ##
csv = []
with open(csv_loc, "r") as f:
    for line in f.readlines():
        csv +=[line.strip().split(",")]
df = pd.DataFrame(csv)
df.columns = df.iloc[0]
df = df.query("gtf == method")

df_depth = df[["build", "depth", "method", "sensitivity", "precision"]]
df_depth[["depth", "precision", "sensitivity"]] = df_depth[["depth", "precision", "sensitivity"]].apply(pd.to_numeric)
df_complexity = df[["build", "depth", "method", "mem", "cpu", "mins"]]
df_complexity[["depth", "mem", "cpu", "mins"]] = df_complexity[["depth", "mem", "cpu", "mins"]].apply(pd.to_numeric)


for m in ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]:
    for b in ["chm13"]:
        df_complexity = pd.concat([pd.DataFrame([[b, 0, m, 0, 0, 0]], columns=df_complexity.columns), df_complexity], ignore_index=True)

max_mem = max(df_complexity["mem"]) + max(df_complexity["mem"])/50
max_cpu = max(df_complexity["cpu"]) + max(df_complexity["cpu"])/50



## main plot layout ##
fig = make_subplots(rows=3, cols=3,
                    specs = [[{"secondary_y" : True, "r": .05}, {"secondary_y" : True, "r" : .05}, {"secondary_y" : True, "r" : .05}],
                             [{"secondary_y" : True, "r" : .05}, {"secondary_y" : True, "r" : .05}, {"secondary_y" : True, "r" : .05}],
                             [{"secondary_y" : True, "r" : .05}, {"secondary_y" : True, "r" : .05}, {"secondary_y" : True, "r" : .05}]],
                     horizontal_spacing=0.05)
fig.update_layout(font_family="Arial", boxmode="group", margin=dict(l=50, r=10, t=80, b=10), showlegend=False)


## name conversion ##
convert = {"ervmap" : "ERVmap",
           "explorate" : "ExplorATE",
           "lions" : "LIONS",
           "squire" : "SQuIRE",
           "te-saem" : "TE-SAEM",
           "telescope" : "Telescope",
           "telocal" : "TElocal",
           "tetools" : "TEtools",
           "texp" : "TeXP"}
colors= ["#ff218c", "#ffd800", "#21b1ff"]

for i, m in enumerate(["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]):
    

## complexity plots ##
    for j, b in enumerate(["chm13"]):
        df_sub = df_complexity.loc[(df_complexity["method"] == m)].reset_index(drop=True)
        mem = list(df_sub["mem"])
        cpu = list(df_sub["cpu"])
        mins = list(df_sub["mins"])
        depth = list(df_sub["depth"])
        
        fig.add_trace(go.Scatter(x=depth, y=mem, name="mem_" + b, line=dict(color=colors[0]), legendrank=1), row=int(i/3)+1, col=(i%3) + 1)
        fig.add_trace(go.Scatter(x=depth, y=cpu, name="cpu_" + b, line=dict(color=colors[2]), legendrank=1), secondary_y=True, row=int(i/3)+1, col=(i%3) + 1)
        fig.add_trace(go.Scatter(x=depth, y=mins, name="mins_" + b, line=dict(color=colors[1]), legendrank=1), secondary_y=True, row=int(i/3)+1, col=(i%3) + 1)


    fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.15, showarrow=False, text=convert[m], row=int(i/3)+1, col=(i%3)+1)

fig.add_annotation(xref="paper", yref="paper", x=0.5, y=1.15, showarrow=False, text="Computational complexity at multiple depths", font=dict(size=18))
fig.add_annotation(xref="paper", yref="paper", x=-0.075, y=.5, showarrow=False, text="GB RAM", font=dict(size=16), textangle=270)
fig.add_annotation(xref="paper", yref="paper", x=1.0, y=.5, showarrow=False, text="Mins to completion", font=dict(size=16), textangle=270)


fig.add_shape(type="rect", xref="paper", yref="paper", x0=.25, x1=.27, y0=1.06, y1=1.08, line=dict(color=colors[1]), fillcolor=colors[1])
fig.add_annotation(xref="paper", yref="paper", x=.28, y=1.09, showarrow=False, text="Wall clock", font=dict(size=14))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.41, x1=.43, y0=1.06, y1=1.08, line=dict(color=colors[2]), fillcolor=colors[2])
fig.add_annotation(xref="paper", yref="paper", x=.50, y=1.09, showarrow=False, text="CPU clock", font=dict(size=14))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.57, x1=.59, y0=1.06, y1=1.08, line=dict(color=colors[0]), fillcolor=colors[0])
fig.add_annotation(xref="paper", yref="paper", x=.63, y=1.09, showarrow=False, text="RAM", font=dict(size=14))



fig.update_xaxes(showgrid=False, showline=True, ticks="inside")
fig.update_yaxes(range=[0, max_mem], secondary_y=False, showgrid=False, ticks="inside")
fig.update_yaxes(range=[0, max_cpu], secondary_y=True, showgrid=False, ticks="inside")


fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)



fig.update_layout(plot_bgcolor="#ffffff")

fig.write_image(width = 600, height=600, file=out_loc, format="png")
