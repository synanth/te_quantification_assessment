import sys
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


base_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/overlap_"
chm13_loc = base_loc + "chm13.txt"
out_loc = "/home/stexocae/data_xfer/heatmap.png"


conversion = {"ervmap": "ERVmap",
              "explorate" : "ExplorATE",
              "lions" : "LIONS",
              "squire" : "SQuIRE",
              "te-saem" : "<b>QuantiTE</b>",
              "telescope" : "Telescope",
              "telocal" : "TElocal",
              "tetools" : "TEtools",
              "texp" : "TeXP"}
methods = ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]
base_nums = {}


## heatmap data massage
d1 = pd.DataFrame(index=[conversion[x] for x in methods], columns=[conversion[x] for x in methods])
with open(chm13_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split(",")
        if buff[0] == buff[1] and buff[0] not in base_nums.keys():
            base_nums[buff[1]] = int(buff[2])
    for line in lines:
        buff = line.strip().split(",")
        d1.loc[conversion[buff[0]], conversion[buff[1]]] = int(buff[2]) / max(base_nums[buff[0]], base_nums[buff[1]])
z_text1 = [[round(y,3) for y in x] for x in d1.values]


## line graphs data massage
csv_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/all.csv"
d = []
with open(csv_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        d += [line.strip().split(",")]
d2 = pd.DataFrame(d)
d2.columns = d2.iloc[0]
d2 = d2.iloc[1:,:8]
d2[["sensitivity", "precision", "f1"]] = d2[["sensitivity", "precision", "f1"]].apply(pd.to_numeric)
d2 = d2.loc[d2["depth"] == "30"].reset_index(drop=True)
d2a = d2.loc[d2["gtf"] == d2["method"]].reset_index(drop=True)
d2b = d2.loc[d2["method"] == "te-saem"].reset_index(drop=True)


## plots ##
fig = make_subplots(rows=5, cols=8, horizontal_spacing=.05, vertical_spacing = 0.01,
                    specs = [[{"colspan":5, "rowspan":5}, None, None, None, None, {"colspan" : 3}, None, None],
                             [None, None, None, None, None, {"rowspan" : 1, "colspan" :3, "b" : 0.05}, None, None],
                             [None, None, None, None, None, {"rowspan" : 1, "colspan" :3}, None, None],
                             [None, None, None, None, None, {"rowspan" : 1, "colspan" :3, "b" : 0.05}, None, None],
                             [None, None, None, None, None, None, None, None]])

fig.update_layout(font_family="Arial", margin=dict(l=10, r=10, t=40, b=10), showlegend=False, boxmode="group")

fig.add_annotation(xref="paper", yref="paper", x=0.5, y=1.2, showarrow=False, text="TE annotation", font=dict(size=18))

## heatmap ##
fig.add_trace(go.Heatmap(z=d1.values, y=d1.index, x=d1.columns, text=z_text1, texttemplate="%{text}", colorscale=["#ffffff", "#7851a9"], showscale=False), row=1, col=1)

fig.add_annotation(xref="paper", yref="paper", x=-0.07, y=1.05, text="A", showarrow=False, font=dict(size=24))

## lineplots ##
colors = ["#74d7ee", "#ffafc8", "#d52d00"]
colors2 = ["#46818f", "#996978", "#a30262"]
fig.add_annotation(xref="paper", yref="paper", x=.628, y=1.05, text="B", showarrow=False, font=dict(size=24))

fig.add_trace(go.Scatter(y=d2b["sensitivity"], x = [conversion[x] for x in d2a["method"]], line=dict(color=colors[0])), row=1, col=6)
fig.add_trace(go.Scatter(y=d2b["sensitivity"], x = [conversion[x] for x in d2a["method"]], line=dict(color=colors[0])), row=2, col=6)
fig.add_trace(go.Scatter(y=d2a["sensitivity"], x = [conversion[x] for x in d2a["method"]], line=dict(color=colors2[0], dash="dot")), row=1, col=6)
fig.add_trace(go.Scatter(y=d2a["sensitivity"], x = [conversion[x] for x in d2a["method"]], line=dict(color=colors2[0], dash="dot")), row=2, col=6)
fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.2, showarrow=False, text="Sensitivity", font=dict(size=14), row=1, col=6)

fig.add_trace(go.Scatter(y=d2b["precision"], x = [conversion[x] for x in d2a["method"]], line=dict(color=colors[1])), row=3, col=6)
fig.add_trace(go.Scatter(y=d2b["precision"], x = [conversion[x] for x in d2a["method"]], line=dict(color=colors[1])), row=4, col=6)
fig.add_trace(go.Scatter(y=d2a["precision"], x = [conversion[x] for x in d2a["method"]], line=dict(color=colors2[1], dash="dot")), row=3, col=6)
fig.add_trace(go.Scatter(y=d2a["precision"], x = [conversion[x] for x in d2a["method"]], line=dict(color=colors2[1], dash="dot")), row=4, col=6)
fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.2, showarrow=False, text="Precision", font=dict(size=14), row=3, col=6)


## legend ##
fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=.1, x1=.2, y0=-1.9, y1=-1.9, line=dict(color="#000000", width = 2), row= 4, col=6)
fig.add_shape(type="circle",  xref="x domain", yref= "y domain", x0=.135, x1=.165, y0=-1.86, y1=-1.94, row=4, col=6, fillcolor="#000000")
fig.add_annotation(xref="x domain", yref="y domain", x=0.23, y=-2.025, showarrow=False, text="TE-SAEM with all annotations", font=dict(size=14), row=4, col=6)


fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=.1, x1=.2, y0=-1.5, y1=-1.5, line=dict(color="#000000", width = 2, dash="dot"), row= 4, col=6)
fig.add_shape(type="circle",  xref="x domain", yref= "y domain", x0=.135, x1=.165, y0=-1.46, y1=-1.54, row=4, col=6, fillcolor="#000000")
fig.add_annotation(xref="x domain", yref="y domain", x=0.21, y=-1.625, showarrow=False, text="Software with native annotation", font=dict(size=14), row=4, col=6)

fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=-.9, showarrow=False, text="GTF", font=dict(size=14), row=4, col=6)


## axis splits ##

fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=-.01, x1=.01, y0=-.03, y1=.03, line=dict(color="#000000", width = 2), row= 1, col=6)
fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=-.01, x1=.01, y0=-.08, y1=-.02, line=dict(color="#000000", width = 2), row= 1, col=6)

fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=.99, x1=1.01, y0=-.03, y1=.03, line=dict(color="#000000", width = 2), row= 1, col=6)
fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=.99, x1=1.01, y0=-.08, y1=-.02, line=dict(color="#000000", width = 2), row= 1, col=6)


fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=-.01, x1=.01, y0=-.03, y1=.03, line=dict(color="#000000", width = 2), row= 3, col=6)
fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=-.01, x1=.01, y0=-.08, y1=-.02, line=dict(color="#000000", width = 2), row= 3, col=6)

fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=.99, x1=1.01, y0=-.03, y1=.03, line=dict(color="#000000", width = 2), row= 3, col=6)
fig.add_shape(type="line", xref = "x domain", yref = "y domain", x0=.99, x1=1.01, y0=-.08, y1=-.02, line=dict(color="#000000", width = 2), row= 3, col=6)


fig.update_yaxes(range=[.95,1.01], row=1, col=6)
fig.update_yaxes(range=[0,.94], row=2, col=6)
fig.update_yaxes(range=[.95,1.01], row=3, col=6)
fig.update_yaxes(range=[0,.94], row=4, col=6)

fig.update_xaxes(showticklabels=False, row=1, col=6)
fig.update_xaxes(showticklabels=False, row=2, col=6)
fig.update_xaxes(showticklabels=False, row=3, col=6)
fig.update_xaxes(tickfont=dict(size=13))
fig.update_yaxes(tickfont=dict(size=13))
fig.update_traces(textfont_size=14)

fig.update_yaxes(autorange="reversed", scaleanchor="x", constrain="domain", row=1, col=1)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

fig.update_layout(plot_bgcolor="#ffffff")
fig.update_yaxes(ticks="inside", mirror=True, row=2, col=6)

fig.write_image(file=out_loc, height=600, width=900, format="png")
