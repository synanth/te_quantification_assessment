from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import sys

csv_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/all.csv"
out_loc = "/home/stexocae/data_xfer/depth.png"


## load csv and wrangle data ##
csv = []
with open(csv_loc, "r") as f:
    for line in f.readlines():
        csv +=[line.strip().split(",")]
df = pd.DataFrame(csv)
df.columns = df.iloc[0]
df = df.query("gtf == method")
df = df[["build", "depth", "method", "sensitivity", "precision", "f1"]]

for m in ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]:
    df = pd.concat([pd.DataFrame([["chm13", 0, m, 0, 0, 0]], columns= df.columns), df], ignore_index=True)

df[["precision", "sensitivity", "f1"]] = df[["precision", "sensitivity", "f1"]].apply(pd.to_numeric)


## main plot layout ##
fig = make_subplots(rows=6, cols=3, horizontal_spacing=0.05, vertical_spacing= 0.005,
                    specs = [[{}, {}, {}],
                             [{"b" : .075}, {"b" : .075}, {"b" : .075}],
                             [{}, {}, {}],
                             [{"b" : .075}, {"b" : .075}, {"b" : .075}],
                             [{}, {}, {}],
                             [{"b" : .075}, {"b" : .075}, {"b" : .075}]])

fig.update_layout(font_family="Arial", boxmode="group", margin=dict(l=60, r=20, t=100, b=0), showlegend=False)


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

colors= ["#74d7ee", "#ffafc8", "#613915"]


for i, m in enumerate(["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]):
    df_method = df.loc[df["method"] == m].reset_index(drop=True)
    
    df_sub = df.loc[df["method"] == m].reset_index(drop=True)
    sensitivity = list(df_method["sensitivity"])
    precision = list(df_method["precision"])
    depth = list(df_method["depth"])
    f1 = list(df_method["f1"])

    fig.add_trace(go.Scatter(x=depth, y=precision, name="dp1", line=dict(color=colors[1]), legendrank=1), row=(int(i/3)+1)*2-1, col=(i%3)+1)
    fig.add_trace(go.Scatter(x=depth, y=precision, name="dp2", line=dict(color=colors[1]), legendrank=1), row=int(i/3)*2+2, col=(i%3)+1)
    fig.add_trace(go.Scatter(x=depth, y=sensitivity, name="ds1", line=dict(color=colors[0]), legendrank=1), row=(int(i/3)+1)*2-1, col=(i%3)+1)
    fig.add_trace(go.Scatter(x=depth, y=sensitivity, name="ds2", line=dict(color=colors[0]), legendrank=1), row=int(i/3)*2+2, col=(i%3)+1)
    fig.add_trace(go.Scatter(x=depth, y=f1, name="df1", line=dict(color=colors[2], dash="longdashdot"), legendrank=1), row=(int(i/3)+1)*2-1, col=(i%3)+1)
    fig.add_trace(go.Scatter(x=depth, y=f1, name="df2", line=dict(color=colors[2], dash="longdashdot"), legendrank=1), row=int(i/3)*2+2, col=(i%3)+1)
    fig.update_yaxes(range=[0,1.05], row=(int(i/3)+1)*2-1, col=(i%3)+1)

    fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.15, showarrow=False, text=convert[m], row=(int(i/3)+1)*2-1, col=(i%3)+1)

    fig.update_yaxes(range=[.95,1.0055555], row=(int(i/3)+1)*2-1, col=(i%3) + 1)
    fig.update_yaxes(range=[0,.94], row=int(i/3)*2+2, col=(i%3) + 1)
    fig.update_xaxes(showticklabels=False, row=(int(i/3)+1)*2-1, col=(i%3)+1)


fig.update_xaxes(showgrid=False, showline=True, ticks="inside")
fig.update_yaxes(showgrid=False, ticks="inside")


fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)


## legend ##
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=1.11, showarrow=False, text="Method's performances based on read depth", font=dict(size=18))
fig.add_annotation(xref="paper", yref="paper", x=-0.07, y=.5, showarrow=False, text="Performance", font=dict(size=16), textangle=270)
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=.01, showarrow=False, text="Depth", font=dict(size=16))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.34, x1=.352, y0=1.048, y1=1.06, line=dict(color=colors[0], width=2), fillcolor=colors[0])
fig.add_annotation(xref="paper", yref="paper", x=0.395, y=1.065, showarrow=False, text="Sensitivity", font=dict(size=14))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.46, x1=.472, y0=1.048, y1=1.06, line=dict(color=colors[1], width=2), fillcolor=colors[1])
fig.add_annotation(xref="paper", yref="paper", x=0.513, y=1.065, showarrow=False, text="Precision", font=dict(size=14))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.56, x1=.572, y0=1.048, y1=1.06, line=dict(color=colors[2], width=2), fillcolor=colors[2])
fig.add_annotation(xref="paper", yref="paper", x=0.615, y=1.065, showarrow=False, text="F1-score", font=dict(size=14))


## axis split ##
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=1, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=1, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=1, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=1, col=1)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=1, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=1, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=1, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=1, col=2)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=1, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=1, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=1, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=1, col=3)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=2, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=2, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=2, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=2, col=1)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=2, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=2, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=2, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=2, col=2)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=2, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=2, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=2, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=2, col=3)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=3, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=3, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=3, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=3, col=1)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=3, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=3, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=3, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=3, col=2)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=3, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=3, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.015, y1=.035, line=dict(color="black", width=2), row=3, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9975, x1=1.0075, y0=-.055, y1=-.005, line=dict(color="black", width=2), row=3, col=3)





fig.update_layout(plot_bgcolor="#ffffff")

fig.write_image(width = 900, height=900, file=out_loc, format="png")
