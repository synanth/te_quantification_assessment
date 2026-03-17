import sys

build = sys.argv[1]
gtf = sys.argv[2]
n_reps = sys.argv[3]
depth = sys.argv[4]

base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/"
sim_loc = base_loc + "sim/sim_counts_matrix.csv"
gtf_loc = base_loc + "sim/subset.gtf"

methods = ["ervmap", "explorate", "lions", "squire", "telescope", "telocal", "te-saem", "tetools", "texp"]


## calculate sensitivity && precision ##
def sensitivity_precision(true, pred):
    diff = [x - y for x, y in zip(true, pred)]
    
    for x in range(0, len(true)):
        fun_tp, fun_fp, fun_fn = 0, 0, 0
        if diff[x] >= 1:
            fun_tp = fun_tp + pred[x]
            fun_fn = fun_fn + diff[x]
        else:
            fun_fp = fun_fp + (-1 * diff[x])
            fun_tp = fun_tp + true[x]
    return (fun_tp, fun_fp, fun_fn)


## convert family ##
convert_fam = {"RNA" : "RNA",
               "centr" : "Other",
               "Alu" : "Alu",
               "Alu-VAR" : "Alu",
               "5S-Deu-L2" : "SINE",
               "hAT-Tip100" : "hAT",
               "hAT-Blackjack" : "hAT",
               "Satellite" : "Satellite",
               "CR1" : "Other",
               "hAT-Charlie" : "hAT",
               "ERV1" : "ERV",
               "ERVL" : "ERV",
               "ERV" : "ERV",
               "DNA" : "DNA",
               "Eulor4" :"Eulor4",
               "TcMar" : "TcMar",
               "L1" : "LINE",
               "ERVK" : "ERV",
               "TcMar-Mariner" : "TcMar",
               "Helitron" : "Helitron",
               "TcMar-Tc2" : "TcMar",
               "L2" : "LINE",
               "RTE-X" : "RTE",
               "Gypsy" : "Gypsy",
               "LTR" : "LTR",
               "PiggyBac" : "PiggyBac",
               "hAT" : "hAT",
               "TcMar-Tigger" : "TcMar",
               "MIR" : "MIR",
               "ERVL-MaLR" : "ERV",
               "RTE-BovB" : "RTE",
               "MamRep564" : "MamRep564",
               "Dong-R4" : "Dong",
               "Merlin" : "Merlin",
               "hAT-Ac" : "hAT",
               "Penelope" : "Penelope",
               "MULE-MuDR" : "Mule",
               "SVA" : "SVA",
               "telo" : "telo",
               "UCON101" : "UCON",
               "UCON87" : "UCON",
               "UCON105" : "UCON",
               "UCON12" : "UCON",
               "hAT-Tag1" : "hAT",
               "UCON19" : "UCON",
               "UCON22" : "UCON",
               "UCON24" : "UCON",
               "UCON25" : "UCON",
               "UCON26" : "UCON",
               "UCON28b" : "UCON",
               "UCON31" : "UCON",
               "UCON34" : "UCON",
               "UCON35" : "UCON",
               "UCON37" : "UCON",
               "UCON44" : "UCON",
               "UCON46" : "UCON",
               "UCON48" : "UCON",
               "UCON4" : "UCON",
               "UCON53" : "UCON",
               "UCON54" : "UCON",
               "UCON59" : "UCON",
               "UCON66" : "UCON",
               "UCON6" : "UCON",
               "UCON70" : "UCON",
               "UCON71_Crp" : "UCON",
               "UCON73" : "UCON",
               "UCON72" : "UCON",
               "UCON77" : "UCON",
               "UCON80_AMi" : "UCON",
               "SINE" : "SINE",
               "UCON85" : "UCON",
               "UCON94" : "UCON",
               "UCON9" : "UCON",
               "Simple_repeat" : "Other",
               "Low_complexity" : "Other",
               "tRNA-RTE" : "RTE",
               "rRNA" : "RNA",
               "srpRNA" : "RNA",
               "Unknown" : "Other",
               "snRNA" : "RNA",
               "tRNA" : "RNA",
               "LTR?" : "LTR",
               "tRNA-Deu" : "RNA",
               "DNA?" : "DNA",
               "scRNA" : "RNA",
               "TcMar-Pogo" : "TcMar",
               "PIF-Harbinger" : "PIF",
               "FLAM" : "FLAM",
               "CR1-3" : "CR1",
               "X7A" : "X7A",
               "L4" : "L4",
               "ERV3-16A3" : "ERV",
               "LTR104" : "LTR",
               "Merlin1" : "Merlin",
               "L2-3" : "L2",
               "PABL" : "PABL",
               "MIR1" : "MIR",
               "Helitron3Na" : "Helitron",
               "UCON71" : "UCON",
               "Plat" : "Plat",
               "LTR106" : "LTR",
               "LTR101" : "LTR",
               "X7B" : "X7B",
               "X6A" : "X6A",
               "PRIMA4" : "PRIMA4",
               "L2-1" : "L2",
               "Penelope1" : "Penelope",
               "Chap1" : "Chap",
               "UCON88" : "UCON",
               "X6B" : "X6B",
               "Kanga2" : "Kanga",
               "UCON41" : "UCON", 
               "Tigger2b" : "Tigger",
               "LTR107" : "LTR",
               "CR1-L3A" : "CR1",
               "UCON1" : "UCON",
               "hAT-N1" : "hAT",
               "LTR102" : "LTR",
               "LTR105" : "LTR",
               "X9" : "X9",
               "ERV24B" : "ERV",
               "UCON57" : "UCON",
               "DNA1" : "DNA",
               "X7C" : "X7C",
               "UCON92" : "UCON",
               "LTR103b" : "LTR",
               "UCON5" : "UCON",
               "Helitron1Nb" : "Helitron",
               "UCON84" : "UCON84",
               "ERV24" : "ERV",
               "UCON40" : "UCON40",
               "HERV4" : "HERV",
               "CR1-12" : "CR1",
               "Mam" : "Mam",
               "X1" : "X1",
               "LTR103" : "LTR103",
               "X8" : "X8",
               "UCON43" : "UCON",
               "CR1-16" : "CR1",
               "Helitron2Na" : "Helitron",
               "Tigger1a" : "Tigger",
               "CR1-13" : "CR1",
               "UCON18" : "UCON",
               "UCON76" : "UCON",
               "UCON47" : "UCON",
               "X2" : "X2",
               "HERV1" : "ERV",
               "UCON75" : "UCON",
               "Helitron1Na" : "Helitron",
               "LTR108d" : "LTR",
               "LTR108e" : "LTR",
               "CR1-L3B" : "CR1",
               "X7D" : "X7",
               "Kolobok" : "Kolobok",
               "Crypton" : "Crypton",
               "L1-Tx1" : "LINE",
               "TcMar-Tc1" : "TcMar",
               "I-Jockey" : "I-Jockey",
               "unrepresented" : "Other",
               "Crypton-A" : "Crypton",
               "acro" : "acro",
               "subtelo" : "subtelo",
               "Unspecified" : "Other",
               "X9a" : "X9",
               "X12" : "X12",
               "GAP" : "GAP",
               "COMP-subunit" : "COMP-subunit",
               "X9b" : "X9",
               "X2a" : "X2",
               "X4b" : "X4",
               "hAT-1" : "hAT",
               "hAT-5" : "hAT",
               "X26" : "X26",
               "LTR108a" : "LTR",
               "HERVE" : "ERV",
               "X22" : "X22",
               "X6b" : "X6",
               "X17" : "X17",
               "X4a" : "X4",
               "X33a" : "X33",
               "SAT-VAR" : "SAT",
               "LTR108c" : "LTR",
               "Chap1a" : "Chap1a",
               "X6a" : "X6",
               "CR1-1" : "CR1",
               "SAT" : "SAT",
               "X5a" : "X5",
               "X11" : "X11",
               "X24" : "X24",
               "MARE11" : "MARE",
               "hAT-4b" : "hAT",
               "UCON16" : "UCON",
               "X20" : "X20",
               "teucerv3" : "teucerv",
               "UCON28a" : "UCON",
               "L2-2" : "LINE",
               "X32" : "X32",
               "UCON20" : "UCON",
               "CR1-11" : "CR1",
               "X10b" : "X10",
               "EUTREP14" : "EUTREP",
               "EUTREP6" : "EUTREP",
               "X30" : "X30",
               "teucerv2" : "teucerv",
               "hAT-N1a" : "hAT",
               "X21" : "X21",
               "UCON64" : "UCON",
               "X5B" : "X5",
               "X2b" : "X2",
               "X34" : "X34",
               "X13" : "X13",
               "MARE9" : "MARE",
               "X15" : "X15",
               "X23" : "X23",
               "UCON60" : "UCON",
               "hAT-hAT19" : "hAT",
               "UCON15" : "UCON",
               "UCON58" : "UCON",
               "UCON28c" : "UCON",
               "UCON27" : "UCON",
               "UCON56" : "UCON",
               "UCON12A" : "UCON",
               "UCON67" : "UCON",
               "UCON38" : "UCON",
               "UCON61" : "UCON",
               "Chompy-6" : "Chompy",
               "UCON65" : "UCON",
               "LTR108b" : "LTR",
               "UCON63" : "UCON",
               "UCON82" : "UCON",
               "CR1-8" : "CR1",
               "UCON17" : "UCON",
               "UCON96" : "UCON",
               "UCON93" : "UCON",
               "REP522" : "REP",
               "Charlie7b" : "Charlie",
               "UCON68" : "UCON",
               "UCON87B" : "UCON",
               "teucerv1" : "teucerv",
               "HERV-Fc1" : "HERV",
               "HERV-Fc2" : "HERV"
               }
    

## get fam information ##
fams = {"unrepresented" : "unrepresented"}
with open(gtf_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        name = buff[buff.index("transcript_id") + 1][1:-2]
        fam_id = buff[buff.index("family_id") + 1][1:-2].replace("?", "")
        fams[name] = convert_fam[fam_id]


## get sim data ##
sim_counts = {}
with open(sim_loc, "r") as f:
    lines = f.readlines()
    for line in lines[1:]:
        buff = line.strip().split(",")
        sim_counts[buff[0]] = [int(x) for x in buff[1:]]
print(sim_counts.items())


## process methods' count matrices ##
precision = {}
sensitivity = {}
for method in methods:
    count_loc = base_loc + "sim/" + method + ".csv"
    out_loc = base_loc + "sim/assess/family_" + method + ".csv"
    tp, fp, fn = 0, 0, 0
    method_confusion = {}
    out = []
    with open(count_loc, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            buff = line.strip().split(",")
            confusion = list(sensitivity_precision(sim_counts[buff[0]], [int(x) for x in buff[1:]]))
            if fams[buff[0]] not in method_confusion.keys():
                method_confusion[fams[buff[0]]] = confusion
            else:
                method_confusion[fams[buff[0]]] = [x+y for x,y in zip(method_confusion[fams[buff[0]]], confusion)]

    method_confusion_list = sorted([[x[0]] + x[1] for x in list(method_confusion.items())], key = lambda x: x[1] + x[2] + x[3], reverse=True)
    total = sum([sum(x[1:]) for x in method_confusion_list])
    
    top = [x[0] for x in method_confusion_list if sum(x[1:])/total >= 0.05]
    top = ["LINE", "Alu", "ERV", "MIR", "hAT"] 
    
    other = [0, 0, 0]
    out2 = {"Alu" : [0,0,0],
            "ERV" : [0,0,0],
            "hAT" : [0,0,0],
            "LINE" : [0,0,0],
            "MIR" : [0,0,0],
            "Other" : [0,0,0]}
    for method in method_confusion.keys():
        if method not in top:
            out2["Other"] = [x+y for x, y in zip(out2["Other"], method_confusion[method])]
        else:
            out2[method] = method_confusion[method]

    
    for fam_id, confusion in out2.items():
        if confusion[0] != 0 or confusion[2] != 0:
            sensitivity = confusion[0] / (confusion[0] + confusion[2])
        else:
            sensitivity = 0
        if confusion[0] != 0 or confusion[1] != 0:
            precision = confusion[0] / (confusion[0] + confusion[1])
        else:
            precision = 0
        out += [",".join([fam_id, str(sensitivity), str(precision)])]
    print(out)

    with open(out_loc, "w") as f:
        for o in out:
            f.write(o + "\n")
