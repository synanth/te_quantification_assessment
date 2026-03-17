import sys
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


## data locs ##
base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/"
data_loc = base_loc + "all.csv"
viz_loc = "/home/stexocae/data_xfer/"


## process csv and wrangle data ##
full_csv = []
with open(data_loc, "r") as f:
    for line in f.readlines():
        full_csv += [line.strip().split(",")]
df = pd.DataFrame(full_csv)
df.columns = df.iloc[0]
df = df.query("gtf == method")
df = df.loc[(df["build"] == "chm13") & (df["depth"] == "30")].reset_index(drop=True)


df_buff = df[["method", "alu_sensitivity", "alu_precision", "erv_sensitivity", "erv_precision", 
                "mir_sensitivity", "mir_precision", "hat_sensitivity", "hat_precision",
                "line_sensitivity", "line_precision", "other_sensitivity", "other_precision"]].values.tolist()
df_family = []
for d in df_buff:
    df_family += [[d[0], "Alu", d[1], d[2]]]
    df_family += [[d[0], "ERV", d[3], d[4]]]
    df_family += [[d[0], "MIR", d[5], d[6]]]
    df_family += [[d[0], "hAT", d[7], d[8]]]
    df_family += [[d[0], "LINE", d[9], d[10]]]
    df_family += [[d[0], "Other", d[11], d[12]]]
df_family = pd.DataFrame(df_family)
df_family.columns = ["method", "family", "sensitivity", "precision"]
df_family[["sensitivity", "precision"]] = df_family[["sensitivity", "precision"]].apply(pd.to_numeric)


df_all = df[["method", "sensitivity", "precision"]]
df_all[["sensitivity", "precision"]] = df_all[["sensitivity", "precision"]].apply(pd.to_numeric)


df_complexity = df[["method", "mins", "mem", "cpu"]]
df_complexity[["mins", "mem", "cpu"]] = df_complexity[["mins", "mem", "cpu"]].apply(pd.to_numeric)

## name conversions ##
name_conversion = {"ervmap": "ERVmap",
                   "explorate" : "ExplorATE",
                   "lions" : "LIONS",
                   "squire" : "SQuIRE",
                   "te-saem" : "TE-SAEM",
                   "telescope" : "Telescope",
                   "telocal" : "TElocal",
                   "tetools" : "TEtools",
                   "texp" : "TeXP"}
df_rows = ["ERVmap", "ExplorATE", "LIONS", "SQuIRE", "TE-SAEM", "Telescope", "TElocal", "TEtools", "TeXP"]

## Make plots ##
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## main layout ##
fig = make_subplots(rows=2, cols=2, 
    specs=[[{"colspan" : 2}, None], 
    [{}, {"secondary_y" : True}]], 

    horizontal_spacing = 0.1,
    vertical_spacing = 0.15)

fig.update_layout(font_family="Arial", boxmode='group', showlegend=False, margin=dict(l=20, r=20, t=50, b=20), xaxis1=dict(domain=[0, 1]), xaxis3=dict(domain=[.5,.95]))


## family divisions ##
for i,fam in enumerate(["Alu", "ERV", "hAT", "LINE", "MIR", "Other"]):
    colors = ["#cd001a", "#ef6a00", "#f2cd00", "#79c300", "#1961ae", "#61007d"]
    dark_colors = ["#66000d", "#773500", "#796600", "#3c6100", "#0c3057", "#30003e"]
    name_loc = [.3135, .4235, .5235, .6235, .7335, .8435]
    df_sub = df_family.loc[df_family['family'] == fam]
    method = [name_conversion[x] for x in list(df_sub["method"])]
    sensitivity = list(df_sub["sensitivity"])
    precision = list(df_sub["precision"])
    for j,m in enumerate(method):
        if sensitivity[j] < precision[j]:
            fig.add_trace(go.Bar(y=[sensitivity[j]], x=[m], name=fam, offsetgroup=i, marker_color=colors[i], zorder=1), row=1, col=1)
            fig.add_trace(go.Bar(y=[precision[j]], x=[m], name="p_" + fam, offsetgroup=i, marker_pattern_shape="x", marker_color=dark_colors[i], marker_line=dict(width=2, color=dark_colors[i]), marker_pattern_bgcolor="#e5ecf6"), row=1, col=1)
        else:
            fig.add_trace(go.Bar(y=[precision[j]], x=[m], name="p_" + fam, offsetgroup=i, marker_pattern_shape="x", marker_color=dark_colors[i], marker_line=dict(width=2, color=dark_colors[i]), marker_pattern_bgcolor="#e5ecf6", zorder=1), row=1, col=1)
            fig.add_trace(go.Bar(y=[sensitivity[j]], x=[m], name=fam, offsetgroup=i, marker_color=colors[i]), row=1, col=1)
    fig.update_traces(marker = dict(line_color=dark_colors[i], pattern_fillmode="replace"), selector=({"name" : "p_" + fam}))
    fig.add_shape(type="rect", xref='x domain', yref='y domain', x0=0.3+i*.1, y0=1.025, x1=0.3085 + i*.1, y1=1.065, line=dict(color=colors[i], width=2), fillcolor=colors[i], row=1, col=1)
    fig.add_annotation(xref='x domain', yref='y domain', x=name_loc[i], y=1.075, text=fam, showarrow=False, row=1, col=1)

fig.update_yaxes(title_text="Performance", showgrid=False, row=1, col=1)

fig.add_annotation(xref="x domain",yref="y domain",x= -.01, y=1.15, showarrow=False, text="<b>A</b>", font=dict(size=30),row=1, col=1)

fig.add_annotation(xref="x domain",yref="y domain",x=0.5, y=1.175, showarrow=False,
                   text="Sensitivity and precision of each TE superfamily", font=dict(size=16),row=1, col=1)

fig.add_shape(type="rect", xref='x domain', yref='y domain', x0=0.0465, y0=1.025, x1=0.055, y1=1.065, line=dict(color="black", width=2,), row=1, col=1)
fig.add_annotation(xref='x domain', yref='y domain', x=0.045, y=1.075, text='X', showarrow=False, row=1, col=1)
fig.add_annotation(xref='x domain', yref='y domain', x=0.06, y=1.075, text='Precision', showarrow=False, row=1, col=1)

fig.add_shape(type="rect", xref='x domain', yref='y domain', x0=0.15, y0=1.025, x1=0.1585, y1=1.065, line=dict(color="black", width=2), fillcolor="black", row=1, col=1)
fig.add_annotation(xref='x domain', yref='y domain', x=0.1635, y=1.075, text='Sensitivity', showarrow=False, row=1, col=1)




## sensitivity and precision ##
raw_precision = list(df_all["precision"])
raw_sensitivity = list(df_all["sensitivity"])

fig.add_trace(go.Scatter(y=raw_precision, x=df_rows, name="Count Precision", marker_color="#F5A9B8"), row=2, col=1)
fig.add_trace(go.Scatter(y=raw_sensitivity, x=df_rows, name="Count Sensitivity", marker_color= "#5BCEFA"), row=2, col=1)

fig.update_yaxes(title_text="Performance", showgrid=False, row=2, col=1)


fig.add_annotation(xref="x domain",yref="y domain",x= -.01, y=1.15, showarrow=False, text="<b>B</b>", font=dict(size=30),row=2, col=1)


fig.add_annotation(xref="x domain",yref="y domain",x=0.5, y=1.175, showarrow=False,
                   text="Overall sensitivity and precision", font=dict(size=16),row=2, col=1)

fig.add_shape(type="line", xref="x domain", yref = "y domain", x0=0.33, y0=1.04, x1=0.39, y1=1.04, line=dict(color="#5bcefa",width=2), row=2, col=1)
fig.add_shape(type="circle", xref="x domain", yref="y domain", x0=0.3552, y0=1.03, x1=0.3648, y1=1.05, line_color="#5bcefa", row=2, col=1)
fig.add_annotation(xref='x domain', yref='y domain', x=0.46, y=1.075, text='Sensitivity', showarrow=False, row=2, col=1)

fig.add_shape(type="line", xref="x domain", yref = "y domain", x0=0.53, y0=1.04, x1=0.59, y1=1.04, line=dict(color="#f5a9b8",width=2), row=2, col=1)
fig.add_shape(type="circle", xref="x domain", yref="y domain", x0=0.5552, y0=1.03, x1=0.5648, y1=1.05, line_color="#f5a9b8", row=2, col=1)
fig.add_annotation(xref='x domain', yref='y domain', x=0.66, y=1.075, text='Precision', showarrow=False, row=2, col=1)
fig.update_yaxes(range=[0,1.1], row=2, col=1)


## time + complexity ##
x = [name_conversion[x] for x in list(df_complexity["method"])]
mem = list(df_complexity["mem"])
mins = list(df_complexity["mins"])
cpu = list(df_complexity["cpu"])

fig.add_trace(go.Scatter(y=mem, x=x, name='RAM', marker_color='#FF218C',), secondary_y=False, row=2, col=2)
fig.add_trace(go.Scatter(y=mins, x=x, name='Wall clock', marker_color='#FFD800',), secondary_y=True, row =2, col=2)
fig.add_trace(go.Scatter(y=cpu, x=x, name='CPU clock', marker_color='#21B1FF',), secondary_y=True, row=2, col=2)

fig.update_yaxes(title_text="GB RAM", showgrid=False, secondary_y=False, row=2, col=2)
fig.update_yaxes(title_text="Minutes to completion", showgrid=False, secondary_y=True, row=2, col=2)

fig.add_annotation(xref="x domain",yref="y domain",x= -.01, y=1.15, showarrow=False, text="<b>C</b>", font=dict(size=30),row=2, col=2)

fig.add_annotation(xref="x domain",yref="y domain",x=0.5, y=1.175, showarrow=False,
                   text="Computational requirements", font=dict(size=16),row=2, col=2)

fig.add_shape(type="rect", xref='x domain', yref='y domain', x0=0.262, y0=1.025, x1=0.278, y1=1.065, line=dict(color="#FFD800", width=2), fillcolor="#FFD800", row=2, col=2)
fig.add_annotation(xref='x domain', yref='y domain', x=0.283, y=1.075, text='Wall clock', showarrow=False, row=2, col=2)

fig.add_shape(type="rect", xref='x domain', yref='y domain', x0=0.472, y0=1.025, x1=0.488, y1=1.065, line=dict(color="#21B1FF", width=2), fillcolor="#21B1FF", row=2, col=2)
fig.add_annotation(xref='x domain', yref='y domain', x=0.553, y=1.075, text='CPU clock', showarrow=False, row=2, col=2)

fig.add_shape(type="rect", xref='x domain', yref='y domain', x0=0.642, y0=1.025, x1=0.658, y1=1.065, line=dict(color="#FF218C", width=2), fillcolor="#FF218C", row=2, col=2)
fig.add_annotation(xref='x domain', yref='y domain', x=0.723, y=1.075, text='RAM', showarrow=False, row=2, col=2)


fig.add_shape(type="rect", xref="x domain", yref="y domain", x0=0, x1=1, y0=0, y1=1, line=dict(color="black", width=1), row=1, col=1)
fig.add_shape(type="rect", xref="x domain", yref="y domain", x0=0, x1=1, y0=0, y1=1, line=dict(color="black", width=1), row=2, col=1)
fig.add_shape(type="rect", xref="x domain", yref="y domain", x0=0, x1=1, y0=0, y1=1, line=dict(color="black", width=1), row=2, col=2)

fig.update_yaxes(rangemode="tozero", row=2, col=2, secondary_y=True)
fig.update_yaxes(rangemode="tozero", row=2, col=2, secondary_y=False)

fig.update_xaxes(showline=True, ticks="inside", linewidth=1, linecolor="black", mirror=True)
fig.update_yaxes(showline=True, ticks="inside", linewidth=1, linecolor="black", mirror=True)
fig.update_layout(plot_bgcolor="#ffffff")




## write output ##
## ^_^ ##
fig.write_image(height= 742, width= 1200, file=viz_loc + "assess.pdf", format="pdf")
