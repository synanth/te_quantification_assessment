import subprocess
import sys

build = sys.argv[1]
base_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/"
if build == "chm13":
    base_loc += "texp2/"
elif build == "hg38":
    base_loc += "texp/"
texp_loc = base_loc + "library/L1HS_hg38/ref/L1HS_hg38.bed"
gtf_base_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/"
out_loc = gtf_base_loc + "simulation/" + build + "/texp.gtf"
tecount_loc = gtf_base_loc + "simulation/" + build + "/tecount.gtf"
buff_loc = gtf_base_loc + "buff"


bedtools_call = "bedtools intersect -wo -a " + texp_loc + " -b " + tecount_loc + " -f 0.25 -r > " + buff_loc
subprocess.call(bedtools_call, shell=True)

chrs = ["chr1", "chr2", "chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX","chrY"]



## get family and class ##
raw_fams = []
with open(buff_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        te_id = buff[3]
        family = buff[17][1:-2]
        te_class = buff[19][1:-2]
        name = buff[13][1:-2]
        strand = buff[10]
        score = -1*int(buff[-1])
        raw_fams += [[te_id, name, family, te_class, strand, score]]
print(len(raw_fams))
## reduce to most accurate element ##
raw_fams = sorted(raw_fams, key=lambda x:(x[0], x[-1]))
seen = set()
fams = {}
for x in raw_fams:
    if x[0] in seen:
        continue
    else:
        seen.add(x[0])
        fams[x[0]] = x[1:]


## make gtf ##
gtf = []
with open(texp_loc, "r") as f:
    lines = f.readlines()
    for l in lines:
        buff = l.strip().split()
        chrom = buff[0]
        start = buff[1]
        end = buff[2]
        te_id = buff[3]
        if te_id not in fams.keys():
            fams[te_id] = [te_id, "L1", "LINE", "+", "0"]
        last_col = " ".join(["gene_id", "\"" + fams[te_id][0] + "\";", "transcript_id", "\"" + te_id + "\";", "family_id", "\"" + fams[te_id][1] + "\";", "class_id", "\"" + fams[te_id][2] + "\";", "gene_name", "\"" + te_id + "\";"])
        out = "\t".join([chrom, "texp", "exon", start, end, ".", fams[te_id][3], ".", last_col])
        gtf += [out]


## write to file ##
with open(out_loc, "w") as f:
    for line in gtf:
        f.write(line + "\n")
