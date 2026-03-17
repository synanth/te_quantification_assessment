import sys

sample = sys.argv[1]
gtf = sys.argv[2]
n_reps = sys.argv[3]
depth = sys.argv[4]
jobid = sys.argv[5]

base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + gtf + "_" + n_reps + "_" + depth + "/sim/"
star_loc = base_loc + sample + "/star_Log.final.out"
bowtie2_loc = "/home/stexocae/li_lab/te_sim/out/align/bowtie2/" + sample + "_" + gtf + "_" + n_reps + "_" + depth+ ".e" + jobid
out_loc = base_loc + "assess/align.csv"


with open(bowtie2_loc, "r") as f:
    lines = f.readlines()
    n_reads = int(lines[1].split()[0])
    one_concordance = str(lines[4].split()[1][1:-2])
    multi_concordance = str(lines[5].split()[1][1:-2])
    once_discordance = str(round(int(lines[8].split()[0])/n_reads,2))
    bowtie_overall = str(lines[-1].split()[0][:-1])

with open(star_loc, "r") as f:
    lines = f.readlines()
    uniquely_mapped = str(float(lines[9].split()[-1][:-1]))
    multimapped_rate = str(float(lines[24].split()[-1][:-1]))
    star_overall = str(round(float(uniquely_mapped) + float(multimapped_rate),2))
    star_unmapped = str(round(100 - float(star_overall), 2))


names = ["sample", "bowtie_once", "bowtie_multi", "bowtie_discord", "bowtie_overall", "star_unique", "star_multi", "star_overall", "star_unmapped"]
out = ",".join([sample, one_concordance, multi_concordance, once_discordance, bowtie_overall, uniquely_mapped, multimapped_rate, star_overall, star_unmapped])

print(names)
print(out)

with open(out_loc, "a") as f:
    f.write(out + "\n")
