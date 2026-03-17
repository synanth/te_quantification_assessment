import sys

build = sys.argv[1]

in_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/backup/" +  build + ".gtf.locInd.locations"
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/hammell/" + build + ".gtf"
out_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/telocal.gtf"  

chroms = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chrX", "chrY"]

## get family et al ##
d = {}
with open(gtf_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        name = buff[9][1:-2]
        items = buff[10:]
        d[name] = items


## process location file ##
gtf = []
with open(in_loc) as f:
    lines = f.readlines()
    for x in lines[1:]:
        buff = x.strip().split()
        name = buff[0].split("_")[0]
        coords = buff[1].split(":")[1].split("-")
        chrom = buff[1].split(":")[0]
        if chrom not in chroms:
            continue
        strand = buff[1].split(":")[-1]
        if name not in d.keys():
            d[name] = ["transcript_id", "\"" + name + "\";", "family_id", "\"" + name + "\";", "class_id", "\"" + name + "\";", "gene_name", "\"" + name + ":TE\";"]
        last_col = " ".join(["gene_id", "\"" + name + "\";", d[name][0], "\"" + buff[0] + "\";"] + d[name][2:])
        out = [chrom, "rmsk", "exon", coords[0], coords[1], ".", strand, ".", last_col]
        gtf += [out]


## write ###
with open(out_loc, "w") as f:
    for line in gtf:
        f.write("\t".join(line) + "\n")
