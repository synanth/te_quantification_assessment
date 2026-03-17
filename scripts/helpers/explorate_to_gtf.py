import sys
import subprocess

build = sys.argv[1]

base_loc = "/lustre/work/stexocae/li_lab/refs/"
rmsk_loc = base_loc + build + "/raw/rmsk.out" 
out_loc = base_loc + "te_annotations/simulation/" + build + "/explorate.gtf"


excluded_classes = ["Unknown", "rRNA", "Satellite", "Simple_repeat","Low_complexity","RNA","scRNA","snRNA","srpRNA", "tRNA","Other"]
chroms = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chrX", "chrY"]


gtf = []
with open(rmsk_loc, "r") as f:
    lines = f.readlines()
    for line in lines[3:]:
        buff = line.strip().split()
        ch = buff[4]
        if ch not in chroms:
            continue
        start = buff[5]
        end = buff[6]
        score = buff[13]
        strand = buff[8].replace("C", "-")
        rep = buff[9]
        class_fam = buff[10].split("/")
        if len(class_fam) == 1:
            class_fam += ["Unknown"]
        class_id = class_fam[0]
        if class_id in excluded_classes:
            continue
        fam = class_fam[1]
        transcript_id = ch + ":" + start + ":" + end + ":" + rep + "/" + class_id + "/" + fam
        last_col = 'gene_id "' + rep + '"; transcript_id "' + transcript_id +'"; family_id "' + fam + '"; class_id "' + class_id + '"; gene_name "' + rep + ':TE";'
        out = "\t".join([ch, "explorate", "exon", start, end, ".", strand, ".", last_col])
        gtf += [out]


## write output ##
with open(out_loc, "w") as f:    
    for line in gtf:
        f.write(line + "\n")
