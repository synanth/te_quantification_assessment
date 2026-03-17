from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import sys

build = "chm13"
color = "#F5A9B8"
dark_color = "#e83a5c"


methods = ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]
convert = {"ervmap" : "ERVmap",
           "explorate" : "ExplorATE",
           "lions" : "LIONS",
           "squire" : "SQuIRE",
           "te-saem" : "TE-SAEM",
           "telescope" : "Telescope",
           "telocal" : "TElocal",
           "tetools" : "TEtools",
           "texp" : "TeXP"}

csv_out = []

colors=["#74d7ee", "#ffafc8"]
## calculate sensitivity && precision ##
def sensitivity_precision(true, pred):
    diff = [x - y for x, y in zip(true, pred)]
    
    for x in range(0, len(true)):
        fun_tp, fun_fp, fun_fn = 0, 0, 0
        if diff[x] >= 1:
            fun_tp = fun_tp + pred[x]
            fun_fn = fun_fn + diff[x]
        else:
            fun_fp = fun_fp + (-1 * diff[x])
            fun_tp = fun_tp + true[x]
    return (fun_tp, fun_fp, fun_fn)
    
## get fam information ##
for gtf in methods:
    base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_1_30/"
    sim_loc = base_loc + "sim/sim_counts_matrix.csv"
    gtf_loc = base_loc + "sim/subset.gtf"
    out_loc = "/home/stexocae/data_xfer/family_" + gtf + ".png"


    fams = {"unrepresented" : "unrepresented"}
    with open(gtf_loc, "r") as f:
        lines = f.readlines()
        for line in lines:
            buff = line.strip().split()
            name = buff[buff.index("transcript_id") + 1][1:-2]
            fam_id = buff[buff.index("family_id") + 1][1:-2].replace("?", "")
            fams[name] = fam_id


    ## get sim data ##
    sim_counts = {}
    with open(sim_loc, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            buff = line.strip().split(",")
            sim_counts[buff[0]] = [int(x) for x in buff[1:]]


    ## setup main plot layout ##
    fig = make_subplots(rows=6, cols=3, vertical_spacing=0.005,
        specs= [[{}, {}, {}],
               [{"b": .075}, {"b" : .075}, {"b": .075}],
               [{}, {}, {}],
               [{"b": .075}, {"b" : .075}, {"b": .075}],
               [{}, {}, {}],
               [{"b": .075}, {"b" : .075}, {"b": .075}]])
    fig.update_layout(font_family="Arial", margin=dict(l=20, r=20, t=100, b=20), showlegend=False)

    ## process methods' count matrices ##
    precision = {}
    sensitivity = {}
    i = 1
    row, col = 1, 1
    for method in methods:
        count_loc = base_loc + "sim/" + method + ".csv"
        tp, fp, fn = 0, 0, 0
        method_confusion = {}
        out = []
        with open(count_loc, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                buff = line.strip().split(",")
                confusion = list(sensitivity_precision(sim_counts[buff[0]], [int(x) for x in buff[1:]]))
                if fams[buff[0]] not in method_confusion.keys():
                    method_confusion[fams[buff[0]]] = confusion
                else:
                    method_confusion[fams[buff[0]]] = [x+y for x,y in zip(method_confusion[fams[buff[0]]], confusion)]

        method_confusion_list = sorted([[x[0]] + x[1] for x in list(method_confusion.items())], key = lambda x: x[1] + x[2] + x[3], reverse=True)
        total = sum([sum(x[1:]) for x in method_confusion_list])
    
        top_names = [x[0] for x in method_confusion_list if sum(x[1:])/total >= 0.001 and x[0] != "unrepresented"]
        top = [x for x in method_confusion_list if x[0] in top_names]

        ## calculate s&p ##
        df = []
        for x in top:
            precision, sensitivity = 0, 0
            if x[1] != 0 or x[2] != 0:
                precision = x[1]/(x[1] + x[2])
            if x[1] != 0 or x[3] != 0:
                sensitivity = x[1] / (x[1] + x[3])
            df += [[x[0], precision, sensitivity]]
        df = pd.DataFrame(df)
        df.columns = ["name", "precision", "sensitivity"]
        df[["precision", "sensitivity"]] = df[["precision", "sensitivity"]].apply(pd.to_numeric)

        ## set up subgraph ##
        name = list(df["name"])
        precision = list(df["precision"])
        sensitivity = list(df["sensitivity"])
        fig.add_trace(go.Bar(y=precision, x=name, marker_color=colors[1]),  row=row, col=col)

        fig.add_trace(go.Bar(y=sensitivity, x=name, marker_color=colors[0]), row=row, col=col)
        fig.add_annotation(xref="x domain", yref="y domain", x=0.5, y=1.1, showarrow=False, text=convert[method], font=dict(size=14), row=row, col=col)
        
        fig.update_xaxes(showticklabels=False, row=row, col=col)

        fig.add_trace(go.Bar(y=precision, x=name, marker_color=colors[1]), row=row+1, col=col)
        fig.add_trace(go.Bar(y=sensitivity, x=name, marker_color=colors[0]), row=row+1, col=col)


        fig.update_yaxes(range=[.95,1.01], row=row, col=col)
        fig.update_yaxes(range=[0,.94], row=row+1, col=col)

        ## axis split ##
        fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.02, y1=.02, line=dict(width=2), row=row, col=col)
        fig.add_shape(type="line", xref="x domain", yref="y domain", x0=-.0075, x1=.0075, y0=-.06, y1=-.02, line=dict(width=2), row=row, col=col)
        fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9925, x1=1.0075, y0=-.02, y1=.02, line=dict(width=2), row=row, col=col)
        fig.add_shape(type="line", xref="x domain", yref="y domain", x0=.9925, x1=1.0075, y0=-.06, y1=-.02, line=dict(width=2), row=row, col=col)
        
        ## update idx ##
        if i % 3 == 0:
            row += 2
        else:
            if col == 3:
                col = 1
            else:
                col += 1 
        i += 1        
        csv_out += [[gtf, method, name, sensitivity, precision ]]


    ## legend ##
    fig.add_annotation(xref="paper", yref="paper", x=0.5, y=1.09, text="TE families' sensitivity and precision for " + convert[gtf] + "'s GTF at 30X", showarrow=False, font=dict(size=20, weight="bold"))


    fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.4, x1=0.41, y0=1.04, y1=1.05, line=dict(color=colors[0], width=2), fillcolor=colors[0])
    fig.add_annotation(xref="paper", yref="paper", x=.44, y=1.055, text="Sensitivity", showarrow=False, font=dict(size=14))

    fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.55, x1=0.56, y0=1.04, y1=1.05, line=dict(color=colors[1], width=2), fillcolor=colors[1])
    fig.add_annotation(xref="paper", yref="paper", x=.59, y=1.055, text="Precision", showarrow=False, font=dict(size=14))



    fig.update_xaxes(showgrid=False, showline=True, ticks="inside", linewidth=1, linecolor="black", mirror=True, tickangle=45)
    fig.update_yaxes(showgrid=False, showline=True, ticks="inside", linewidth=1, linecolor="black", mirror=True)
    fig.update_layout(plot_bgcolor="#ffffff")

    print(out_loc)
    fig.write_image(height=1200, width=1200, file = out_loc, format="png")
quit()



families = []
for x in csv_out:
    families += x[2]
    for e, fam in enumerate(x[2]):
        x[2][e] += "," + str(x[3][e]) + "," + str(x[4][e])
families = sorted(list(set(families)))
out = [["gtf", "method"] + families + ["avg_sensitivity", "avg_precision"]]

for x in csv_out:
    buff = [x[0], x[1]]
    fams = [y.split(",")[0] for y in x[2]]
    avg_s = 0
    avg_p = 0
    n_fam = 0
    for y in out[0][2:-2]:
        try:
            buff2 = [str(round(float(q),4)) for q in x[2][fams.index(y)].split(",")[1:]]
            avg_s += float(buff2[0])
            avg_p += float(buff2[1])
            n_fam += 1
            val = "_".join(buff2)
        except:
            val = str(0)
        buff += [val]
    out += [buff + [str(round(avg_s/n_fam,2)), str(round(avg_p/n_fam,2))]]
out_loc = "/home/stexocae/li_lab/te_sim/out/families.csv"

with open(out_loc, "w") as f:
    for x in out:
        f.write(",".join(x) + "\n")
