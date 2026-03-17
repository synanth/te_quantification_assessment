import sys

build = sys.argv[1]
out_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/squire.gtf"
loc_base = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/SQuIRE/squire/squire_clean/"
if build == "chm13":
    in_loc = loc_base + "hs1_all.bed"
else:
    in_loc = loc_base + build + "_all.bed"

chroms = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12",
          "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chrX",
          "chrY"]


## make gtf from bed ##
num_seen = {}
gtf = []
with open(in_loc, "r") as f:
    lines = f.readlines()
    for l in lines:
        buff = l.strip().split()
        chrom = buff[0]
        if chrom not in chroms:
            continue
        start = buff[1]
        end = buff[2]
        score = buff[4]
        strand = buff[5]
        buff2 = buff[3].split("|")[3].split(":")
        name = buff2[0]
        family = buff2[1]
        te_class = buff2[2]
        if name not in num_seen.keys():
            num_seen[name] = 1
        else:
            num_seen[name] = num_seen[name] + 1
        te_id = name + "_dup" + str(num_seen[name])
        last_col = " ".join(["gene_id", "\"" + name + "\";", "transcript_id", "\"" + te_id + "\";", "family_id", "\"" + family +"\";", "class_id", "\"" + te_class + "\";", "gene_name", "\"" + name + ":TE\";"])
        out = "\t".join([chrom, "rmsk", "exon", start, end, score, strand, ".", last_col])
        gtf += [out]


with open(out_loc, "w") as f:
    for line in gtf:
        f.write(line + "\n")
