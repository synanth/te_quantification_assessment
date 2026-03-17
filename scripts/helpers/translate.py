import subprocess
import sys

build = sys.argv[1]
in_method = sys.argv[2]
out_method = sys.argv[3]

base = "/lustre/work/stexocae/li_lab/refs/te_annotations/"

if build == "chm13":
    locs = {"ervmap" : base + "simulation/chm13/ervmap.gtf",
        "explorate" : base + "backup/chm13_rmsk.bed",
        "lions" : base + "simulation/chm13/lions.gtf",
        "squire" : base + "simulation/chm13/squire.gtf",
        "superset" : base + "simulation/chm13/superset.gtf",
        "tecount" : base + "hammell/chm13.gtf",
        "telescope" : base + "simulation/chm13/telescope.gtf",
        "telocal" : base + "backup/telocal_chm13.gtf",
        "tetools" : "/lustre/work/stexocae/li_lab/refs/chm13/raw/hs1_all.bed",
        "texp" : "/home/stexocae/li_lab/te_sim/scripts/quant/packages/texp2/library/L1HS_hg38/ref/L1HS_hg38.bed",
        "saem" : base + "simulation/chm13/saem.gtf"}

    lens = {"ervmap" : 18,
        "explorate" : 15,
        "lions" : 18,
        "squire" : 18,
        "superset" : 18,
        "tecount" : 18,
        "telescope" : 18,
        "telocal" : 12,
        "tetools" : 9,
        "texp" : 4,
        "saem" : 22}
elif build == "hg38":
    locs = {"ervmap" : base + "simulation/hg38/ervmap.gtf",
        "explorate" : base + "backup/hg38_rmsk.bed",
        "lions" : base + "simulation/hg38/lions.gtf",
        "squire" : base + "simulation/hg38/squire.gtf",
        "superset" : base + "simulation/hg38/superset.gtf",
        "tecount" : base + "hammell/hg38.gtf",
        "telescope" : base + "simulation/hg38/telescope.gtf",
        "telocal" : base + "backup/telocal_hg38.gtf",
        "tetools" : "/lustre/work/stexocae/li_lab/refs/hg38/raw/hg38_all.bed",
        "texp" : "/home/stexocae/li_lab/te_sim/scripts/quant/packages/texp/library/L1HS_hg38/ref/L1HS_hg38.bed"}

    lens = {"ervmap" : 18,
        "explorate" : 15,
        "lions" : 18,
        "squire" : 18,
        "superset" : 18,
        "tecount" : 18,
        "telescope" : 18,
        "telocal" : 12,
        "tetools" : 9,
        "texp" : 4}


def get_transcripts_loc(m, l):
    if m == "ervmap":
        ret = l[11][1:-2]
    elif m == "explorate":
        ret = l[0] + ":" + str(int(l[1])+1) + ":" + l[2] + ":" + l[3] + "/" + l[10]
    elif m == "lions":
        ret = l[11][1:-2]
    elif m == "squire":
        ret = l[11][1:-2]
    elif m == "superset":
        ret = l[11][1:-2]
    elif m == "tecount":
        ret = "_".join(l[11][1:-2].split("_")[:-1]) + ":" + l[13][1:-2] + ":" + l[15][1:-2]
    elif m == "telescope":
        ret = l[11][1:-2]
    elif m == "telocal":
        ret = l[11][2:-4]
    elif m == "tetools":
        ret = l[3]
    elif m == "texp":
        ret = l[3]
    elif m == "saem":
        ret = l[11][1:-2]
    return(ret)


## data management ##
in_folder = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/"
buff_loc = in_folder + "buff"
in_method_loc = locs[in_method]
out_method_loc = locs[out_method]
out_loc = in_folder + "translations/" + build + "/" + in_method + "_to_" + out_method + ".txt"

## superset creation ##
get_nonrepresented_tes_call = "bedtools intersect -wo -a " + in_method_loc + " -b " + out_method_loc + " -f 0.25 -r > " + buff_loc
subprocess.call(get_nonrepresented_tes_call, shell=True)



translation = []
with open(buff_loc, 'r') as f:
    d = f.readlines()
    for x in d:
        buff = x.strip().split()
        in_annotation = buff[:lens[in_method]]
        out_annotation = buff[lens[in_method]:-1]
        translation += [[get_transcripts_loc(in_method, in_annotation), get_transcripts_loc(out_method, out_annotation), -1* int(buff[-1])]]

translation = sorted(translation, key=lambda x: (x[0], x[-1]))
seen = set()
out = []
for x in translation:
    if x[0] in seen:
        continue
    else:
        seen.add(x[0])
        out += [x[0] + "," + x[1] + "\n"]

with open(out_loc, "w") as f:
    for x in out:
        f.write(x)
