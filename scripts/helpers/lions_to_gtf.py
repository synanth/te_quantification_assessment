import sys

build = sys.argv[1]
in_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/LIONS/resources/" + build + "/repeat/rm_" + build + ".ucsc"
out_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/lions.gtf"

chrs = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chrX", "chrY"]

num_seen = {}
gtf = []
with open(in_loc, "r") as f:
    lines = f.readlines()
    for line in lines[1:]:
        buff = line.strip().split()
        score = buff[1]
        chrom = buff[5]
        if chrom not in chrs:
            continue
        start = buff[6]
        end = buff[7]
        strand = buff[9]
        name = buff[10]
        te_class = buff[11]
        family = buff[12]
        if end <= start:
            continue
        if start == 0 or start == "0":
            print("wtf")
            continue
        if name not in num_seen.keys():
            num_seen[name] = 1
        else:
            num_seen[name] = num_seen[name] + 1
        te_id = name + "_dup" + str(num_seen[name])
        last_col = " ".join(["gene_id", "\"" + name + "\";", "transcript_id", "\"" + te_id + "\";", "family_id", "\"" + family + "\";", "class_id", "\"" + te_class + "\";", "gene_name", "\"" + name + ":TE\";"])
        out = "\t".join([chrom, "rmsk", "exon", start, end, score, strand, ".", last_col])
        
        gtf += [out]


with open(out_loc, "w") as f:
    for line in gtf:
        f.write(line + "\n")
