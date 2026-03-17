import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_de = sys.argv[4]
depth = sys.argv[5]

working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/"
sim_loc = working_dir + "sim/" + sample + "/"
program_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/TEtools/TEcount.py"

rosette_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/tetools/" + build + ".txt"
te_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/tetools/" + build + ".fa"

sam_loc = sim_loc + "star_sorted.sam"
fasta_loc1 = sim_loc + sample + "_R1.fq"
fasta_loc2 = sim_loc + sample + "_R2.fq"
out_loc = working_dir + "tetools/" + sample
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/tetools.py"


## copy te and rosette loc to working folder ##
cp1_call = "cp " + te_loc + " " + out_loc
cp2_call = "cp " + rosette_loc + " " + out_loc
subprocess.run(cp1_call, shell=True)
subprocess.run(cp2_call, shell=True)





tetools_call = "python " + program_loc + " -rosette=" + rosette_loc + " "
tetools_call += "-column=2 -TE_fasta=" + te_loc + " "
tetools_call += "-count=" + out_loc + " "
tetools_call += " -RNA=" + fasta_loc1 + " " 
tetools_call += "-RNApair=" + fasta_loc2

subprocess.run(tetools_call, shell=True)


## translate ##
translate_call = "python3 " + translate_loc + " " + build + " " + gtf + " " + sample + " " + n_de + " " + depth
subprocess.run(translate_call, shell=True)

## clean up ##
#rm_call = "rm -rf " + out_loc + "*"
#subprocess.run(rm_call, shell=True)
