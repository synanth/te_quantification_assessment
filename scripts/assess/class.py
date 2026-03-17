import sys

build = sys.argv[1]
gtf = sys.argv[2]
n_reps = sys.argv[3]
depth = sys.argv[4]

base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/"
sim_loc = base_loc + "sim/sim_counts_matrix.csv"
gtf_loc = base_loc + "sim/subset.gtf"

methods = ["ervmap", "explorate", "lions", "squire", "telescope", "telocal", "tetools", "texp"]
methods = ["telocal"]


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
fams = {"unrepresented" : "unrepresented"}
with open(gtf_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        name = buff[buff.index("transcript_id") + 1][1:-2]
        fam_id = buff[buff.index("class_id") + 1][1:-2]
        fams[name] = fam_id


## get sim data ##
sim_counts = {}
with open(sim_loc, "r") as f:
    lines = f.readlines()
    for line in lines[1:]:
        buff = line.strip().split(",")
        sim_counts[buff[0]] = [int(x) for x in buff[1:]]


## process methods' count matrices ##
precision = {}
sensitivity = {}
for method in methods:
    count_loc = base_loc + "sim/" + method + ".csv"
    out_loc = base_loc + "sim/assess/family_" + method + ".csv"
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
    for fam_id, confusion in method_confusion.items():
        if confusion[0] != 0 or confusion[2] != 0:
            sensitivity = confusion[0] / (confusion[0] + confusion[2])
        else:
            sensitivity = 0
        if confusion[0] != 0 or confusion[1] != 0:
            precision = confusion[0] / (confusion[0] + confusion[1])
        else:
            precision = 0
        out += [",".join([fam_id, str(sensitivity), str(precision)])]
    print(out)
    quit()
    with open(out_loc, "w") as f:
        for o in out:
            f.write(o + "\n")
