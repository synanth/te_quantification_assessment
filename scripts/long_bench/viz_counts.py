from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

base_loc = "/home/stexocae/data_xfer/"
csv_loc = base_loc + "longbench_counts.csv"
viz_loc = base_loc + "longbench_counts.png"
names = {"ervmap" : "ERVmap", "explorate" : "ExplorATE", "lions" : "LIONS", 
         "squire" : "SQuIRE", "te-saem" : "TE-SAEM", "telescope" : "Telescope", 
         "telocal" : "TElocal", "tetools" : "TEtools", "texp" : "TeXP"}


df = pd.read_csv(csv_loc)

fig = make_subplots(rows=1, cols=1)
fig.update_layout(font_family="Arial", showlegend=False, 
                  margin={"l" : 20, "r" : 20, "t" : 80, "b" : 20})

for x in names:
    df_sub = df[df["method"] == x]
    fig.add_trace(go.Box(y=df_sub["n_map"], name=x))

fig.write_image(file=viz_loc, format="png")
