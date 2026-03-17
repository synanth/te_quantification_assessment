

depths = [2, 5, 10, 30, 50]
samples = ["sample_01", "sample_02"]

base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/chm13_te-saem_1_"
gtf_loc = "/home/stexocae/li_lab/saem/refs/hs1.gtf"

tele1 = {}
tele2 = {}
true = {}
tes = set()
out = [["depth", "te-saem_precision", "te-saem_sensitivity", "te-saem_f1", "telescope_precision", "telescope_sensitivity", "telescope_f1"]]


## get set of tes ##
with open(gtf_loc, "r") as f:
    for line in f.readlines():
        buff = line.strip().split()
        tes.add(buff[11][1:-2])


## get results ##
for x in depths:
    true_loc = base_loc + str(x) + "/sim/sim_counts_matrix.csv"
    tele_loc1 = base_loc + str(x) + "/telescope/supp_sample_01/counts.txt"
    tele_loc2 = base_loc + str(x) + "/telescope/supp_sample_02/counts.txt"
    saem_loc = base_loc + str(x) + "/sim/assess/raw_te-saem.csv"
    out_buff = [x, 0, 0, 0, 0, 0, 0]
    
    with open(saem_loc, "r") as f:
        for line in f.readlines()[1:]:
            buff = line.strip().split(",")
            out_buff[1] = buff[2]
            out_buff[2] = buff[1]
            out_buff[3] = buff[3]

    with open(tele_loc1, "r") as f:
        for line in f.readlines():
            if line.split(",")[0] == "unrepresented":
                continue
            buff = line.strip().split(",")
            tele1[buff[0]] = int(buff[1])

    with open(tele_loc2, "r") as f:
        for line in f.readlines():
            if line.split(",")[0] == "unrepresented":
                continue
            buff = line.strip().split(",")
            tele2[buff[0]] = int(buff[1])


    with open(true_loc, "r") as f:
        for line in f.readlines()[1:]:
            buff = line.strip().split(",")
            true[buff[0]] = [int(x) for x in buff[1:]]

## calculate results ##
    tp, fp, fn = 0, 0, 0

    for te in tes:
        if tele1.get(te, 0) - true.get(te, [0,0])[0] > 0:
            tp += true.get(te, [0,0])[0]
            fp += tele1.get(te, 0) - true.get(te, [0,0])[0]
        else:
            tp += tele1.get(te, 0)
            fn += true.get(te, [0,0])[0] - tele1.get(te, 0)
        
        if tele2.get(te, 0) - true.get(te, [0,0])[1] > 0:
            tp += true.get(te, [0,0])[0]
            fp += tele2.get(te, 0) - true.get(te, [0,0])[0]
        else:
            tp += tele2.get(te, 0)
            fn += true.get(te, [0,0])[0] - tele1.get(te, 0)
    sensitivity = tp /(tp+fn)
    precision = tp/(tp+fp) 
    f1 = (2*precision*sensitivity) / (sensitivity+precision)
    out_buff[4] = precision 
    out_buff[5] = sensitivity
    out_buff[6] = f1
    print(out_buff)
    out += [out_buff]
print(out)

## write output ##
out_loc = "/home/stexocae/li_lab/te_sim/supp_tele.csv"

with open(out_loc, "w") as f:
    for line in out:
        f.write(",".join([str(x) for x in line]) + "\n")
