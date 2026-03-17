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

df_depth = df[["build", "depth", "method", "sensitivity", "precision"]]
df_depth[["depth", "precision", "sensitivity"]] = df_depth[["depth", "precision", "sensitivity"]].apply(pd.to_numeric)
df_complexity = df[["build", "depth", "method", "mem", "cpu"]]
df_complexity[["depth", "mem", "cpu"]] = df_complexity[["depth", "mem", "cpu"]].apply(pd.to_numeric)


for m in ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]:
    for b in ["chm13"]:
        df_depth = pd.concat([pd.DataFrame([[b, 0, m, 0, 0]], columns=df_depth.columns), df_depth], ignore_index=True)
        df_complexity = pd.concat([pd.DataFrame([[b, 0, m, 0, 0]], columns=df_complexity.columns), df_complexity], ignore_index=True)

df = df.loc[df["depth"] == "30"].reset_index(drop=True)
df_buff = df[["build", "method", "alu_sensitivity", "alu_precision", "erv_sensitivity", "erv_precision",
              "hat_sensitivity", "hat_precision", 
              "line_sensitivity", "line_precision", 
              "mir_sensitivity", "mir_precision", "other_sensitivity", "other_precision"]].values.tolist()

df_family = []
for d in df_buff:
    df_family += [[d[0], d[1], "Alu", d[2], d[3]]]
    df_family += [[d[0], d[1], "ERV", d[4], d[5]]]
    df_family += [[d[0], d[1], "hAT", d[6], d[7]]]
    df_family += [[d[0], d[1], "LINE", d[8], d[9]]]
    df_family += [[d[0], d[1], "MIR", d[10], d[11]]]
    df_family += [[d[0], d[1], "Other", d[12], d[13]]]

df_family = pd.DataFrame(df_family)
df_family.columns = ["build", "method", "family", "sensitivity", "precision"]
df_family[["precision", "sensitivity"]] = df_family[["precision", "sensitivity"]].apply(pd.to_numeric)




## main plot layout ##
fig = make_subplots(rows=6, cols=3, horizontal_spacing=0.05, vertical_spacing= 0.005,
                    specs = [[{}, {}, {}],
                             [{"b" : .075}, {"b" : .075}, {"b" : .075}],
                             [{}, {}, {}],
                             [{"b" : .075}, {"b" : .075}, {"b" : .075}],
                             [{}, {}, {}],
                             [{"b" : .075}, {"b" : .075}, {"b" : .075}]])

fig.update_layout(font_family="Arial", boxmode="group", margin=dict(l=60, r=20, t=20, b=0), showlegend=False)


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
    df_method = df_family.loc[df_family["method"] == m].reset_index(drop=True)
    
## depth plots ##
    for j, b in enumerate(["chm13"]):
        df_sub = df_depth.loc[(df_depth["method"] == m) & (df_depth["build"] == b)].reset_index(drop=True)
        sensitivity = list(df_sub["sensitivity"])
        precision = list(df_sub["precision"])
        depth = list(df_sub["depth"])

        fig.add_trace(go.Scatter(x=depth, y=precision, name="dp_" + b, line=dict(color=colors[1]), legendrank=1), row=(int(i/3)+1)*2-1, col=(i%3)+1)
        fig.add_trace(go.Scatter(x=depth, y=precision, name="dp_" + b, line=dict(color=colors[1]), legendrank=1), row=int(i/3)*2+2, col=(i%3)+1)
        fig.add_trace(go.Scatter(x=depth, y=sensitivity, name="ds_" + b, line=dict(color=colors[0]), legendrank=1), row=(int(i/3)+1)*2-1, col=(i%3)+1)
        fig.add_trace(go.Scatter(x=depth, y=sensitivity, name="ds_" + b, line=dict(color=colors[0]), legendrank=1), row=int(i/3)*2+2, col=(i%3)+1)
        fig.update_yaxes(range=[0,1.05], row=(int(i/3)+1)*2-1, col=(i%3)+1)

    fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.15, showarrow=False, text=convert[m], row=(int(i/3)+1)*2-1, col=(i%3)+1)

    fig.update_yaxes(range=[.95,1.0055555], row=(int(i/3)+1)*2-1, col=(i%3) + 1)
    fig.update_yaxes(range=[0,.94], row=int(i/3)*2+2, col=(i%3) + 1)



fig.update_xaxes(showgrid=False, showline=True, ticks="inside")
fig.update_yaxes(showgrid=False, ticks="inside")


fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)



fig.update_layout(plot_bgcolor="#ffffff")

fig.write_image(width = 900, height=900, file=out_loc, format="png")
