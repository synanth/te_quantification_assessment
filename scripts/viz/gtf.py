import sys
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/all.csv"
viz_loc = "/home/stexocae/data_xfer/gtf.png"

d = []
with open(base_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        d += [line.strip().split(",")]
df = pd.DataFrame(d)
df.columns = df.iloc[0]
df = df.iloc[1:]
df[["sensitivity", "precision", "f1"]] = df[["sensitivity", "precision", "f1"]].apply(pd.to_numeric)


convert_name = {"ervmap" : "ERVmap",
                "explorate" : "ExplorATE",
                "lions" : "LIONS",
                "squire" : "SQuIRE",
                "te-saem" : "TE-SAEM",
                "telescope" : "Telescope",
                "telocal" : "TElocal",
                "tetools" : "TEtools",
                "texp" : "TeXP"}
methods = ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]


## main plot attributes ##
fig = make_subplots(rows=6, cols=3, horizontal_spacing=0.05, vertical_spacing=0.005, 
                    specs = [[{},{},{}],
                             [{"b": .075},{"b" : .075},{"b" : .075}],
                             [{},{},{}],
                             [{"b": .075},{"b" : .075},{"b" : .075}],
                             [{},{},{}],
                             [{"b": .075},{"b" : .075},{"b" : .075}]])
fig.update_layout(font_family="Arial", boxmode='group', margin=dict(l=20, r=20, t=100, b=20), showlegend=False)

df = df.loc[df["depth"] == "30"].reset_index(drop=True)
colors = ["#74d7ee", "#ffafc8", "#613915"]


for i, m in enumerate(methods):
    df_method = df.loc[df["gtf"] == m].reset_index(drop=True)
    df_build = df_method.loc[df_method["build"] == "chm13"].reset_index(drop=True)
    fig.add_trace(go.Scatter(y=df_build["precision"], x = [convert_name[x] for x in df_build["method"]], line=dict(color=colors[1])), row=(int(i/3)+1)*2-1, col=(i%3)+1)
    fig.add_trace(go.Scatter(y=df_build["precision"], x = [convert_name[x] for x in df_build["method"]], line=dict(color=colors[1])), row=int(i/3)*2+2, col=(i%3)+1)

    fig.add_trace(go.Scatter(y=df_build["sensitivity"], x = [convert_name[x] for x in df_build["method"]], marker_color=colors[0]), row=(int(i/3) + 1)*2-1, col=(i%3)+1)
    fig.add_trace(go.Scatter(y=df_build["sensitivity"], x = [convert_name[x] for x in df_build["method"]], marker_color=colors[0]), row=int(i/3) *2+2, col=(i%3)+1)

    fig.add_trace(go.Scatter(y=df_build["f1"], x = [convert_name[x] for x in df_build["method"]], line=dict(color=colors[2], dash="longdashdot")), row=(int(i/3) + 1)*2-1, col=(i%3)+1)
    fig.add_trace(go.Scatter(y=df_build["f1"], x = [convert_name[x] for x in df_build["method"]], line=dict(color=colors[2], dash="longdashdot")), row=int(i/3) *2+2, col=(i%3)+1)

    fig.update_yaxes(range=[.95,1.01], row= (int(i/3)+1)*2-1, col=(i%3)+1)
    fig.update_yaxes(range=[0,.94], row= int(i/3)*2+2, col=(i%3)+1)

    fig.add_annotation(xref="x domain", yref="y domain", x= 0.5, y=1.15, showarrow=False, text=convert_name[m], row=(int(i/3)+1)*2-1, col=(i%3)+1)

    fig.update_xaxes(showticklabels=False, row=(int(i/3)+1)*2-1, col=(i%3)+1)

fig.update_yaxes(title_text="", row=1, col=1)


## legend ##
fig.add_annotation(xref="paper", yref="paper", x=0.5, y= 1.08, showarrow=False, text="Methods' performances based on annotation files", font=dict(size=18))
fig.add_annotation(xref="paper", yref="paper", x=-0.05, y= .5, showarrow=False, text="Performance", font=dict(size=16), textangle=270)

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.35, x1=.362, y0=1.035, y1=1.045, line=dict(color=colors[0], width=2), fillcolor=colors[0])
fig.add_annotation(xref="paper", yref="paper", x=.397, y=1.0495, showarrow=False, text="Sensitivity", font=dict(size=14))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.463, x1=.475, y0=1.035, y1=1.045, line=dict(color=colors[1], width=2), fillcolor=colors[1])
fig.add_annotation(xref="paper", yref="paper", x=.507, y=1.0495, showarrow=False, text="Precision", font=dict(size=14))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=.57, x1=.582, y0=1.035, y1=1.045, line=dict(color=colors[2], width=2), fillcolor=colors[2])
fig.add_annotation(xref="paper", yref="paper", x=.617, y=1.0495, showarrow=False, text="F1-score", font=dict(size=14))


## axis split ##
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=1, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=1, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=1, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=1, col=1)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=1, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=1, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=1, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=1, col=2)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=1, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=1, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=1, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=1, col=3)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=3, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=3, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=3, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=3, col=1)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=3, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=3, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=3, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=3, col=2)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=3, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=3, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=3, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=3, col=3)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=5, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=5, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=5, col=1)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=5, col=1)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=5, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=5, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=5, col=2)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=5, col=2)

fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=5, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.005, x1=.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=5, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.02, y1=.02, line=dict(color="black", width=2), row=5, col=3)
fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.995, x1=1.005, y0=-.05, y1=-.01, line=dict(color="black", width=2), row=5, col=3)



## boxes ##
fig.update_xaxes(showgrid=False, showline=True, ticks="inside", linewidth=1, linecolor="black", mirror=True)
fig.update_yaxes(showgrid=False, ticks="inside", showline=True, linewidth=1, linecolor="black", mirror=True)
fig.update_layout(plot_bgcolor="#ffffff")


fig.write_image(height=1200, width=1200, file=viz_loc, format="png")
