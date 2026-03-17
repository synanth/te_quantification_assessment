import sys
import subprocess

srr = sys.argv[1]

working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
texp_dir = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/texp2"
texp_loc =  texp_dir + "/TeXP.sh"
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/texp.py"


in_fasta_1 = working_dir + srr + "_1.fastq"
in_fasta_2 = working_dir + srr + "_2.fastq"
out_loc = working_dir + "texp"

texp_call = "bash " + texp_loc + " -f " + in_fasta_1 + " "
texp_call += "-t 16 -o " + out_loc + " -n " + srr

subprocess.run("mkdir " + out_loc, shell=True)
subprocess.run(texp_call, cwd=texp_dir, shell=True)

## translate ##
raw_bed_loc = out_loc + "/" + srr + "/" + srr + ".re.filtered.bed"
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/texp.gtf"
final_counts_loc = out_loc +  "/final_counts.csv"
bedtools_out_loc = out_loc + srr + ".bedtools.out"
out_counts = {}

bedtools_call = "bedtools intersect -f 0.25 -r -wo -a " + raw_bed_loc + " -b " + gtf_loc + " > " + bedtools_out_loc
subprocess.run(bedtools_call, shell=True)

with open(bedtools_out_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        name = buff[28][1:-2]
        if name not in out_counts:
            out_counts[name] = 1
        else:
            out_counts[name] += 1

with open(final_counts_loc, "w") as f:
    for k,v in out_counts.items():
        f.write(k + "," + str(v) + "\n")
