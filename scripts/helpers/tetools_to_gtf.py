import sys
import subprocess

build = sys.argv[1]

base_loc = "/lustre/work/stexocae/li_lab/refs/"
rosette_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/tetools/" + build + ".txt"
out_loc = base_loc + "te_annotations/simulation/" + build + "/tetools.gtf"


chrs = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chrX", "chrY"]

gtf = []
with open(rosette_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()[0].split("|")
        ch = buff[0]
        if ch not in chrs:
            continue
        start = buff[1]
        end = buff[2]
        score = buff[4]
        strand = buff[5]
        rep_class_fam = buff[3].split(":")
        rep = rep_class_fam[0]
        class_id = rep_class_fam[2]
        fam = rep_class_fam[1]

        transcript_id = "|".join(buff)
        last_col = 'gene_id "' + rep + '"; transcript_id "' + transcript_id +'"; family_id "' + fam + '"; class_id "' + class_id + '"; gene_name "' + rep + ':TE";'
        out = "\t".join([ch, "explorate", "exon", start, end, score, strand, ".", last_col])
        gtf += [out]


## write output ##
with open(out_loc, "w") as f:    
    for line in gtf:
        f.write(line + "\n")
