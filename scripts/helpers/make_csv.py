class Wildcard:
    def __eq__(self, anything):
        return True

base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/"
csv_loc = base_loc + "all.csv"

methods = ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]
depths = ["2", "5", "10", "30", "50"]
builds = ["chm13"]
n_reps = "1"

csv_out = []
raw_locs = []
complexity_locs = []
family_locs = []
align_locs = []
csv_out = [["build", "gtf", "n_reps", "depth", "method", "sensitivity", "precision", "f1", "spearmans", 
           "alu_sensitivity", "alu_precision", "erv_sensitivity", "erv_precision",
           "hat_sensitivity", "hat_precision",
           "line_sensitivity", "line_precision", "mir_sensitivity", "mir_precision", 
           "other_sensitivity", "other_precision",
           "mins", "mem", "n_cpu", "cpu"]]

for build in builds:
    for gtf in methods:
        for depth in depths:
            folder_loc = base_loc + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/assess/"
            for method in methods:
                raw_locs += [folder_loc + "raw_" + method + ".csv"]
                complexity_locs += [folder_loc + "complexity_" + method + ".csv"]
                family_locs += [folder_loc + "family_" + method + ".csv"]
            align_locs += [folder_loc + "complexity_bowtie2.csv"]
            align_locs += [folder_loc + "complexity_star.csv"]

need_to_fix = []
for loc in raw_locs:
    method = loc.split("/")[-1].split("_")[1][:-4]
    build, gtf, n_reps, depth = loc.split("/")[6].split("_")
    try:
        with open(loc, "r") as f:
            spearman, sensitivity, precision, f1 = f.readlines()[1].strip().split(",")
            csv_out += [[build, gtf, n_reps, depth, method, sensitivity, precision, f1, spearman]]
    except:
        need_to_fix += [loc]
wc = Wildcard()

for loc in family_locs:
    method = loc.split("/")[-1].split("_")[1][:-4]
    build, gtf, n_reps, depth = loc.split("/")[6].split("_")
    try:
        with open(loc, "r") as f:
            idx =csv_out.index([build, gtf, n_reps, depth, method, wc, wc, wc, wc])
            buff = sum([x.strip().split(",")[1:] for x in f.readlines()], [])
            csv_out[idx] += buff
    except:
        need_to_fix += [loc]

align = []
for loc in align_locs:
    method = loc.split("/")[-1].split("_")[1][:-4]
    build, gtf, n_reps, depth = loc.split("/")[6].split("_")
    try:
        with open(loc, "r") as f:
            buff = [[float(y) for y in x.strip().split(",")[2:]] for x in f.readlines()]
            buff = [sum(x)/2 for x in zip(buff[0], buff[1])]
            align += [[build, gtf, n_reps, depth, method] + buff]
    except:
        need_to_fix += [loc]
for loc in complexity_locs:
    method = loc.split("/")[-1].split("_")[1][:-4]
    build, gtf, n_reps, depth = loc.split("/")[6].split("_")
    try:
        with open(loc, "r") as f:
            idx = csv_out.index([build, gtf, n_reps, depth, method, wc, wc, wc, wc, wc, wc, wc, wc, wc, wc, wc, wc, wc, wc, wc, wc])
            buff = [[float(y) for y in x.strip().split(",")[2:]] for x in f.readlines()]
            buff = [sum(x)/2 for x in zip(buff[0], buff[1])]
            if method == "telocal":
                a = [float(x) for x in align[align.index([build, gtf, n_reps, depth, "star", wc, wc ,wc ,wc])][-4:]]
                buff = [sum(x) for x in zip(buff, a)]
            elif method == "telescope":
                a = [float(x) for x in align[align.index([build, gtf, n_reps, depth, "bowtie2", wc, wc ,wc ,wc])][-4:]]
                buff = [sum(x) for x in zip(buff, a)]
            csv_out[idx] += buff
    except Exception as e:
        need_to_fix += [loc]


for x in need_to_fix:
    print(x)
with open(csv_loc, "w") as f:
    for line in csv_out:
        f.write(",".join([str(x) for x in line]) + "\n")
