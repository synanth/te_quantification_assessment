import sys
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


## data locs ##
data_loc = "/home/stexocae/li_lab/te_sim/supp_tele.csv"
viz_loc = "/home/stexocae/data_xfer/supp_tele.png"

d = []
## process csv and wrangle data ##
with open(data_loc, "r") as f:
    for line in f.readlines():
        d += [line.strip().split(",")]
df = pd.DataFrame(d)
df.columns = df.iloc[0]
df = df.drop(index=0, axis=0).reset_index(drop=True)
df[["depth", "te-saem_precision", "te-saem_sensitivity", "te-saem_f1", "telescope_precision", "telescope_sensitivity", "telescope_f1"]] = df[["depth", "te-saem_precision", "te-saem_sensitivity", "te-saem_f1", "telescope_precision", "telescope_sensitivity", "telescope_f1"]].apply(pd.to_numeric)


## name conversions ##
name_conversion = {"te-saem" : "TE-SAEM",
                   "telescope" : "Telescope"}

## Make plots ##
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## main layout ##
fig = make_subplots(rows=1, cols=3, 
    specs=[[{}, {}, {}]],
    horizontal_spacing = 0.05,
    vertical_spacing = 0.01)

fig.update_layout(font_family="Arial", boxmode='group', showlegend=False, margin=dict(l=70, r=20, t=100, b=50))


## sensitivity and precision ##

fig.add_trace(go.Scatter(y=df["te-saem_sensitivity"], x=df["depth"], name="Sensitivity", marker_color="#74d7ee"), row=1, col=1)
fig.add_trace(go.Scatter(y=df["te-saem_precision"], x=df["depth"], name="Precision", marker_color="#ffafc8"), row=1, col=2)
fig.add_trace(go.Scatter(y=df["te-saem_f1"], x=df["depth"], name="F1", marker_color="#613915"), row=1, col=3)


fig.add_trace(go.Scatter(y=df["telescope_sensitivity"], x=df["depth"], marker_color="#74d7ee", line=dict(dash="dot")), row=1, col=1)
fig.add_trace(go.Scatter(y=df["telescope_precision"], x=df["depth"], marker_color="#ffafc8", line=dict(dash="dot")), row=1, col=2)
fig.add_trace(go.Scatter(y=df["telescope_f1"], x=df["depth"], marker_color="#613915", line=dict(dash="dot")), row=1, col=3)


fig.update_yaxes(range=[.85, 1.005], showgrid=False, row=1, col=1)
fig.update_yaxes(range=[.85, 1.005], showgrid=False, row=1, col=2)
fig.update_yaxes(range=[.85, 1.005], showgrid=False, row=1, col=3)





## subplot outlines ##
fig.add_shape(type="rect", xref="x domain", yref="y domain", x0=0, x1=1, y0=0, y1=1, line=dict(color="black", width=1), row=1, col=1)
fig.add_shape(type="rect", xref="x domain", yref="y domain", x0=0, x1=1, y0=0, y1=1, line=dict(color="black", width=1), row=1, col=2)
fig.add_shape(type="rect", xref="x domain", yref="y domain", x0=0, x1=1, y0=0, y1=1, line=dict(color="black", width=1), row=1, col=3)


fig.add_annotation(xref="paper", yref="paper", x=-.07, y=0.5, showarrow=False, text="Preformance", font=dict(size=16), textangle=270)
fig.add_annotation(xref="paper", yref="paper", x=.5, y=-0.15, showarrow=False, text="Depth", font=dict(size=16))
fig.add_annotation(xref="paper", yref="paper", x=.5, y=1.3, showarrow=False, text="Comparison between TE-SAEM and Telescope using TE-SAEM's GTF", font=dict(size=20))

fig.add_annotation(xref= "x domain", yref="y domain", x=0.5, y=1.1, showarrow=False, text="Sensitivity", font=dict(size=16), row=1, col=1)
fig.add_annotation(xref= "x domain", yref="y domain", x=0.5, y=1.1, showarrow=False, text="Precision", font=dict(size=16), row=1, col=2)
fig.add_annotation(xref= "x domain", yref="y domain", x=0.5, y=1.1, showarrow=False, text="F1-Score", font=dict(size=16), row=1, col=3)

fig.add_shape(type="line", xref="paper", yref="paper", x0=0.35, x1=.4, y0=1.15, y1=1.15, line=dict(width=2))
fig.add_shape(type="circle", xref="paper", yref="paper", x0=0.37, x1=.38, y0=1.135, y1=1.165, line=dict(width=2), fillcolor="#000000")

fig.add_annotation(xref="paper", yref="paper", x=.45, y=1.185, text="TE-SAEM", font=dict(size=14), showarrow=False)

fig.add_shape(type="line", xref="paper", yref="paper", x0=0.55, x1=.6, y0=1.15, y1=1.15, line=dict(width=2, dash="dot"))
fig.add_shape(type="circle", xref="paper", yref="paper", x0=0.57, x1=.58, y0=1.135, y1=1.165, line=dict(width=2), fillcolor="#000000")
fig.add_annotation(xref="paper", yref="paper", x=.65, y=1.185 ,showarrow=False,  text="Telescope", font=dict(size=14))




fig.update_yaxes(showline=True, ticks="inside", linewidth=1, linecolor="black", mirror=True)
fig.update_layout(plot_bgcolor="#ffffff")




## write output ##
## ^_^ ##
fig.write_image(height= 450, width= 900, file=viz_loc, format="png")
