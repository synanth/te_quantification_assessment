import subprocess
from pyliftover import LiftOver

base_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/"
chain_loc = base_loc + "chain/grch38-chm13v2.chain"
texp_loc = base_loc + "bed/L1HS_hg38.bed"
out_loc = base_loc + "simulation/texp.gtf"
buff_loc = base_loc + "bed/texp_chm13.bed"


lo = LiftOver(chain_loc)

out = []
with open(texp_loc, "r") as f:
    lines = f.readlines()
    print(len(lines))
    for l in lines[100:]:
        buff = l.strip().split()
        if not lo.convert_coordinate(buff[0], int(buff[1])) or not lo.convert_coordinate(buff[0], int(buff[2])):
            continue
        chrm = buff[0]
        coord1 = str(lo.convert_coordinate(buff[0], int(buff[1]))[0][1])
        coord2 = str(lo.convert_coordinate(buff[0], int(buff[2]))[0][1])
        tools = "bedtools"
        method = "transcript"
        if int(coord1) >= int(coord2):
            continue
        gene_id = "gene_id \"" + buff[3] + ":" + chrm + ":" + coord1 + ":" + coord2 + "\"; " + "transcript_id \"" + buff[3] + ":" + chrm + ":" + coord1 + ":" + coord2 + "\";"
        out += [[chrm, tools, method, coord1, coord2, ".", "+", ".", gene_id]]
print(len(out))
print(out[:5])

with open(out_loc, "w") as f:
    for x in out:
        buff = "\t".join(x)
        f.write(buff + "\n")
