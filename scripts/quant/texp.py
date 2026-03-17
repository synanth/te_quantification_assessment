import os
import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_de = sys.argv[4]
depth = sys.argv[5]

working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/"
sim_loc = working_dir + "sim/" + sample + "/"
if build == "chm13":
    texp_dir = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/texp2"
elif build == "hg38":
    texp_dir = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/texp"
else:
    print("Build must be chm13 or hg38.")
    sys.exit()
texp_loc =  texp_dir + "/TeXP.sh"
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/texp.py"


os.chdir(texp_dir)

in_fasta_1 = sim_loc + sample + "_R1.fq"
in_fasta_2 = sim_loc + sample + "_R2.fq"
out_loc = working_dir + "texp"

texp_call = "bash " + texp_loc + " -f " + in_fasta_1 + " "
texp_call += "-t 8 -o " + out_loc + " -n " + sample

subprocess.run(texp_call, cwd=texp_dir, shell=True)


## translate ##
translate_call = "python3 " + translate_loc + " " + build + " " + gtf + " " + sample + " " + n_de + " " + depth
subprocess.run(translate_call, shell=True)

## clean up ##
#rm_call = "rm -rf " + out_loc + "/" + sample + "*"
#subprocess.run(rm_call, shell=True)
