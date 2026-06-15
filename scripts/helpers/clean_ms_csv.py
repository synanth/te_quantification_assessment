

csv_loc = "/home/stexocae/data_xfer/ms_degs.csv"
out_loc = "/home/stexocae/data_xfer/ms_degs_threshold.csv"
out = []

with open(csv_loc, "r") as f:
    lines = f.readlines()
    out += [lines[0]]
    for line in lines[1:]:
        buff = line.strip().split(",")
        if buff[-2] == "NA":
            continue
        pval = float(buff[-2])
        if pval <= .1:
            out += [line]

with open(out_loc, "w") as f:
    for line in out:
        f.write(line)
