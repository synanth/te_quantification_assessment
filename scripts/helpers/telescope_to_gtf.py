from pyliftover import LiftOver
import subprocess

base_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/"
loc = base_loc + "bendall/transcripts.gtf"
chain_loc = base_loc + "chain/grch38-chm13v2.chain"

out_hg38_loc = base_loc + "bendall/hg38.gtf"
out_chm13_loc = base_loc + "bendall/chm13.gtf"
sim_hg38_loc = base_loc + "simulation/hg38/telescope.gtf"
sim_chm13_loc = base_loc + "simulation/chm13/telescope.gtf"

tecount_loc = base_loc + "simulation/hg38/telocal.gtf"
buff_loc = base_loc + "buff"

chroms = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chr21", "chr22", "chrX", "chrY"]



## get families ##
bedtools_call = "bedtools intersect -wo -a " + loc + " -b " + tecount_loc + " -f 0.25 -r > " + buff_loc
subprocess.run(bedtools_call, shell=True)

raw_fams = []
with open(buff_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        if line[0] == "#":
            continue
        buff = line.strip().split()
        te_id = buff[9][1:-2]
        family = buff[-6][1:-2]
        te_class = buff[-4][1:-2]
        name = buff[-10][1:-2]
        score = buff[-1]
        raw_fams += [[te_id, family, te_class, -1*int(score)]]


## reduce to highest scoring ##
raw_fams = sorted(raw_fams, key=lambda x: (x[0], x[-1]))
seen = set()
fams = {}
for f in raw_fams:
    if f[0] in seen:
        continue
    seen.add(f[0])
    fams[f[0]] = f[1:]
lo = LiftOver(chain_loc)

sim_hg38 = []
sim_chm13 = []


with open(loc, "r") as f:
    lines = f.readlines()
    for l in lines:
        if l[0] =="#":
            continue
        buff = l.strip().split("\t")
        if buff[0] not in chroms:
            continue
        last_col = buff[8].split()[:4]
        if last_col[2] in fams:
            family = fams[last_col[2]][0]
            te_class = fams[last_col[1]][0]
        else:
            family = "ERV"
            te_class = "ERV"
        last_col += ["family_id", '"' + family + '";', "class_id", '"' + te_class + '";', "gene_name" , last_col[1]]
        buff = buff[:8] + [" ".join(last_col)]
        
        if buff[2] == "gene":
            sim_hg38 += ["\t".join(buff)]

        if lo.convert_coordinate(buff[0], int(buff[3])) and lo.convert_coordinate(buff[0], int(buff[4])):
            coord1 = str(lo.convert_coordinate(buff[0], int(buff[3]))[0][1])
            coord2 = str(lo.convert_coordinate(buff[0], int(buff[4]))[0][1])
            chm13_buff = buff
            chm13_buff[3] = coord1
            chm13_buff[4] = coord2
            if coord2 < coord1:
                continue
            if chm13_buff[2] == "gene":
                sim_chm13 += ["\t".join(chm13_buff)]

with open(sim_hg38_loc, "w") as f:    
    for o in sim_hg38:
        f.write(o + "\n")

with open(sim_chm13_loc, "w") as f:    
    for o in sim_chm13:
        f.write(o + "\n")
