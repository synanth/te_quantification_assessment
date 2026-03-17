import sys
import subprocess

build = "chm13"
gtf = "te-saem"
sample = sys.argv[1]
n_de = str(1)
depth = sys.argv[2]

working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/"
sample_loc = working_dir + "sim/" + sample + "/bowtie2.bam"
out_dir = working_dir + "telescope/supp_" + sample 
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/telescope.py"

gene_gtf_loc = "/lustre/work/stexocae/li_lab/refs/chm13/raw/chm13.gtf"
te_gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/te-saem.gtf"
    

telescope_call = "telescope assign --theta_prior 200000 --max_iter 200 --outdir "
telescope_call += out_dir + " " + sample_loc + " " + te_gtf_loc + " 2>&1 | tee " + out_dir + "_tele.log"

subprocess.run("mkdir " + out_dir, shell=True)
subprocess.run(telescope_call, shell=True)


## translate ##
counts_loc = out_dir + "/telescope-telescope_report.tsv"
tes = set()
with open(te_gtf_loc, "r") as f:
    for line in f.readlines():
        buff = line.strip().split()
        tes.add(buff[11][1:-2])
counts = {"unrepresented" : 0}
with open(counts_loc, "r") as f:
    for line in f.readlines()[3:]:
        buff = line.strip().split()
        if buff[0] not in tes:
            counts["unrepresented"] += int(buff[2])
        else:
            counts[buff[0]] = int(buff[2])
new_loc = out_dir + "/counts.txt"

with open(new_loc, "w") as f:
    for k,v in counts.items():
        f.write(k + "," + str(v) + "\n")

