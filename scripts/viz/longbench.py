from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np

data_loc = "/home/stexocae/data_xfer/longbench.csv"
count_loc = "/home/stexocae/data_xfer/longbench_counts.csv"
other_loc = "/lustre/research/dawli/stexocaelum/longbench/other_gtf.csv"
viz_loc = "/home/stexocae/data_xfer/longbench.png"
convert_name = {"ervmap" : "ERVmap", 
                "explorate" : "ExplorATE",
                "lions" : "LIONS",
                "squire" : "SQuIRE",
                "te-saem" : "<b>QuantiTE</b>",
                "telescope" : "Telescope",
                "telocal" : "TElocal",
                "tetools" : "TEtools",
                "texp" : "TeXP"}

colors = {"ervmap" : "#ff00ff", 
          "explorate" : "#ff0040",
          "lions" : "#ff9500",
          "squire" : "#f0c808",
          "te-saem" : "#6100ff",
          "telescope" : "#aaff00",
          "telocal" : "#00ffff",
          "tetools" : "#0095ff",
          "texp" : "#00ff15"}

legend_loc = [0, .11, .22, .33, .44, .55, .66, .77, .88]
legend_name_loc = [.0152, .125, .24, .38, .496, .61, .74, .85, .941]


df = pd.read_csv(data_loc)
df_counts = pd.read_csv(count_loc)
df["n_map"] = df_counts["n_map"]
df_other = pd.read_csv(other_loc)

## make figures ##
fig = make_subplots(rows=4, cols=4, horizontal_spacing=.07, vertical_spacing=.05,
                    specs=[[{"colspan" : 2}, None, {"colspan" : 2}, None],
                           [{"colspan" : 2}, None, {"colspan" : 2}, None],
                           [{}, {}, {}, {}],
                           [{}, {}, {}, {}]],
                    row_heights = [.39, .39, .01, .21]) 
fig.update_layout(font_family="Arial", boxmode="group", showlegend=False, margin=dict(l=20, r=20, t=80, b=20), plot_bgcolor= "#ffffff", boxgap=.1, boxgroupgap=0)
fig.update_xaxes(tickfont_size=12, linewidth=1, showline=True, linecolor="black", mirror=True, ticks="inside")
fig.update_yaxes(tickfont_size=12, linewidth=1, showline=True, linecolor="black", mirror=True, ticks="inside")


# main longbench plot #
for e,x in enumerate(convert_name):
    df_sub = df[df["method"] == x]
    fig.add_trace(go.Scatter(y=df_sub["pearson"], x=df_sub["n_map"], mode="markers", marker_color=colors[x], opacity=.3), row=1, col=1)
    fig.add_trace(go.Scatter(y=[float(df_sub["pearson"].mean())], x=[float(df_sub["n_map"].mean())], mode="markers", marker_color=colors[x], marker_symbol="square", marker_size=10), row=1, col=1)
    fig.add_trace(go.Scatter(y=df_sub["spearman"], x=df_sub["n_map"], mode="markers", marker_color=colors[x], opacity=.3), row=1, col=3)
    fig.add_trace(go.Scatter(y=[float(df_sub["spearman"].mean())], x=[float(df_sub["n_map"].mean())], mode="markers", marker_color=colors[x], marker_symbol="square", marker_size=10), row=1, col=3)
    fig.add_trace(go.Scatter(y=df_sub["mae"], x=df_sub["n_map"], mode="markers", marker_color=colors[x], opacity=.3), row=2, col=1)
    fig.add_trace(go.Scatter(y=[float(df_sub["mae"].mean())], x=[float(df_sub["n_map"].mean())], mode="markers", marker_color=colors[x], marker_symbol="square", marker_size=10), row=2, col=1)
    fig.add_trace(go.Scatter(y=df_sub["rmse"], x=df_sub["n_map"], mode="markers", marker_color=colors[x], opacity=.3), row=2, col=3)
    fig.add_trace(go.Scatter(y=[float(df_sub["rmse"].mean())], x=[float(df_sub["n_map"].mean())], mode="markers", marker_color=colors[x], marker_symbol="square", marker_size=10), row=2, col=3)
    
    fig.add_shape(type="rect", xref="paper", yref="paper", x0=legend_loc[e], x1=legend_loc[e]+.015, y0=1.07, y1=1.085, fillcolor=colors[x])
    fig.add_annotation(xref="paper", yref="paper", text=convert_name[x], font={"size" : 14}, y=1.09, x=legend_name_loc[e], showarrow=False)

fig.add_shape(type="circle", xref="paper", yref="paper", x0=.3 , x1=.315 , y0=1.025 , y1=1.04 , fillcolor="#666666")
fig.add_annotation(xref="paper", yref="paper", text="Individual Sample", font={"size" : 14}, x=.32, y=1.045, showarrow=False)
fig.add_shape(type="rect", xref="paper", yref="paper", x0=.5, x1=.515, y0=1.025, y1=1.04, fillcolor="black")
fig.add_annotation(xref="paper", yref="paper", text="Samples' Mean", font={"size" : 14}, x=.577, y=1.045, showarrow=False)


fig.add_annotation(xref="paper", yref="paper", text="Number assigned reads", showarrow=False, x=0.5, y=.23, font={"size" : 16})
fig.update_yaxes(title_text="Pearson's", row=1, col=1)
fig.update_yaxes(title_text="Spearman's", row=1, col=3)
fig.update_yaxes(title_text="MAE", row=2, col=1)
fig.update_yaxes(title_text="RMSE", row=2, col=3)

## using other annotations ##
df_gtf = df_other[df_other["gtf"] == "ervmap"] 
for y in ["ervmap", "te-saem"]:
    df_sub = df_gtf[df_gtf["method"] == y]
    fig.add_trace(go.Box(y=df_sub["mae"], name="MAE", marker_color=colors[y], offsetgroup=y), row=4, col=1)
    fig.add_trace(go.Box(y=df_sub["rmse"], name="RMSE", marker_color=colors[y], offsetgroup=y), row=4, col=1)
    fig.add_trace(go.Box(y=df_sub["pearson"], name="Pearson's", marker_color=colors[y], offsetgroup=y), row=4, col=2)
    fig.add_trace(go.Box(y=df_sub["spearman"], name="Spearman's", marker_color=colors[y], offsetgroup=y), row=4, col=2)

df_gtf = df_other[df_other["gtf"] == "telescope"] 
for y in ["telescope", "te-saem"]:
    df_sub = df_gtf[df_gtf["method"] == y]
    fig.add_trace(go.Box(y=df_sub["mae"], name="MAE", marker_color=colors[y], offsetgroup=y), row=4, col=3)
    fig.add_trace(go.Box(y=df_sub["rmse"], name="RMSE", marker_color=colors[y], offsetgroup=y), row=4, col=3)
    fig.add_trace(go.Box(y=df_sub["pearson"], name="Pearson's", marker_color=colors[y], offsetgroup=y), row=4, col=4)
    fig.add_trace(go.Box(y=df_sub["spearman"], name="Spearman's", marker_color=colors[y], offsetgroup=y), row=4, col=4)



fig.add_annotation(xref="paper", yref="paper", text="A", x=-.02, y =1.05, font_size=24, showarrow=False)
fig.add_annotation(xref="paper", yref="paper", text="B", x=-.02, y =.18, font_size=24, showarrow=False)
fig.add_annotation(xref="paper", yref="paper", text="C", x=.52, y =.18, font_size=24, showarrow=False)

fig.write_image(height=900, width=900, file=viz_loc, format="png")
