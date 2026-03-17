import sys
import subprocess

build = sys.argv[1]

base_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/"
tecount_loc = base_loc + "simulation/" + build + "/telocal.gtf"
ervmap_loc = base_loc + "bed/ervmap_" + build + ".bed"
buff_loc = base_loc + "buff"
buff2_loc = base_loc + "buff2"
out_loc = base_loc + "simulation/" + build + "/ervmap.gtf"

convert_call = "bedToGenePred " + ervmap_loc + " /dev/stdout | genePredToGtf file /dev/stdin " + buff_loc
subprocess.call(convert_call, shell=True)

bedtools_call = "bedtools intersect -wa -wb -a " + buff_loc + " -b " + tecount_loc + " -f 0.25 -r > " + buff2_loc
subprocess.call(bedtools_call, shell=True)
chroms=["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chrX", "chrY"]


## find family and class based up tecount ##
fams = {}
with open(buff2_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        if buff[2] != "transcript":
            continue
        te_id = buff[9][1:-2]
        name = buff[21][1:-2]
        fam = buff[25][1:-2]
        te_class = buff[27][1:-2]
        fams[te_id] = [name, fam, te_class]


## construct gtf ##
gtf = []
with open(buff_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        if buff[2] != "transcript":
            continue
        chrom = buff[0]
        if chrom not in chroms:
            continue
        start = buff[3]
        end = buff[4]
        score = buff[5]
        strand = buff[6]
        te_id = buff[9][1:-2]
        if te_id not in fams.keys():
            fams[te_id] = [te_id, "ERV", "ERV"]
        last_col = " ".join(["gene_id", "\"" + fams[te_id][0] + "\";", "transcript_id", "\"" + te_id + "\";", "family_id", "\"" + fams[te_id][1] + "\";", "class_id", "\"" + fams[te_id][2] + "\";", "gene_name", "\"" + te_id + ":TE\";"])
        out = "\t".join([chrom, "ervmap", "exon", start, end, score, strand, ".", last_col])
        gtf += [out]


## write output ##
with open(out_loc, "w") as f:    
    for line in gtf:
        f.write(line + "\n")
