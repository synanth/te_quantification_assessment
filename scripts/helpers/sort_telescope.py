base_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/"
new_loc = base_loc + "telescope.gtf"
old_loc = base_loc + "telescope_backup2.gtf"

old_gtf = []
chr_order = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8",
             "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16",
             "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chr23",
             "chrX", "chrY"]


with open(old_loc, "r") as f:
    for line in f.readlines():
        buff = line.strip().split("\t")
        old_gtf += [buff]

new_gtf = sorted(old_gtf, key = lambda x: (int(x[0][3:]) if x[0][3:].isnumeric() else ord(x[0][3:]), int(x[3])))


with open(new_loc, "w") as f:
    for line in new_gtf:
        f.write("\t".join(line) + "\n")
