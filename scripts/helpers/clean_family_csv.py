
csv_loc = "/home/stexocae/data_xfer/families.csv"
out_loc = "/home/stexocae/data_xfer/clean_families.csv"


out = []

with open(csv_loc, "r") as f:
    lines = f.readlines()
    buff = lines[0].strip().split(",")
    index = ["gtf", "method"]
    for x in buff[2:-2]:
        index += [x + "_sensitivity", x + "_precision"]
    index += ["avg_sensitivity", "avg_precision"]
    out += [index]
    for line in lines[1:]:
        buff = line.strip().split(",")
        buff2 = [buff[0], buff[1]]
        for x in buff[2:-2]:
            if x == '0':
                buff2 += ['0','0']
            else:
                buff2 += x.split("_")
        buff2 += [buff[-2], buff[-1]]
        out += [buff2]

with open(out_loc, "w") as f:
    for line in out:
        f.write(",".join(line) + "\n")
