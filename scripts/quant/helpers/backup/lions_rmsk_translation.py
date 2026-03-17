
in_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/chm13_rmsk.out"
out_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/LIONS/resources/chm13/repeat/rm_chm13.ucsc"


out = [["#bin", "swScore", "milliDiv", "milliDel", "milliIns", "genoName", "genoStart", "genoEnd", "genoLeft", "strand", "repName", "repClass", "repFamily", "repStart", "repEnd", "repLeft", "id"]]
with open(in_loc, "r") as f:
   lines = f.readlines()
   for x in lines[3:]:
    buff = x.strip().split()
    if '(' in buff[7]:
        buff[7] = '-' + buff[7][1:-1]
    if '/' in buff[10]:
        repClass, repFamily = buff[10].split('/')
    else:
        repClass = buff[10]
        repFamily = buff[10]
    if buff[8] == 'C':
        buff[8] = '-'
    if '(' in buff[13]:
        buff[13] = '-' + buff[13][1:-1]
    out += [['0', buff[0], str(int(float(buff[1])*10)), str(int(float(buff[2])*10)), str(int(float(buff[3])*10)), buff[4], buff[5], buff[6], buff[7], buff[8], buff[9], repClass, repFamily, buff[11], buff[12], buff[13], buff[14]]]

with open(out_loc, "w") as f:
    for x in out:
        f.write("\t".join(x) + "\n")
