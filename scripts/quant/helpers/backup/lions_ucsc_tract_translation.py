
lions_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/LIONS/resources/chm13/annotation/"
in_loc = lions_loc + "ncbirefSeq.bed"
out_loc = lions_loc + "refseq_chm13.ucsc"

out = [["bin", "name", "chrom", "strand", "txStart", "txEnd", "cdsStart", "cdsEnd", "exonCount", "exonStarts", "exonEnds", "score", "name2", "cdsStartStat", "cdsEndStat", "exonFrames"]]
with open(in_loc, "r") as f:
    lines = f.readlines()
    for l in lines[1:]:
        buff = l.strip().split()
        block_sizes = buff[10].strip(',').split(',')
        exon_ends = [(x,y) for x,y in enumerate(buff[11][:-1].split(','))]
        exon_ends = ','.join([str(int(x[1]) + int(block_sizes[x[0]])) for x in exon_ends]) + ','
        out += [['0', buff[3], buff[0], buff[5], buff[1], buff[2], buff[6], buff[7], buff[9], buff[11], exon_ends, buff[4], buff[12], buff[13], buff[14], buff[15]]]

with open(out_loc, "w") as f:
    for x in out:
        f.write('\t'.join(x) + "\n")
