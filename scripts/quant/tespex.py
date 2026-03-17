import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_de = sys.argv[4]
depth = sys.argv[5]

## file management ##
working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/"
tespex_dir = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/TEspeX/"
tespex_loc =  tespex_dir + "TEspeX.py"

if build == "chm13":
    te_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/tespex/homo_sapiens.fa"
    cdna_loc = tespex_dir + "data/gencode.v47.transcripts.fa.gz"
    ncrna_loc = tespex_dir + "data/gencode.v47.lncRNA_transcripts.fa.gz"
    index_loc = "/lustre/work/stexocae/li_lab/refs/chm13/star/"
elif build == "hg38":
    te_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/tespex/repbase.fa"
    cdna_loc = tespex_dir + "data/gencode.v47.transcripts.fa.gz"
    ncrna_loc = tespex_dir + "data/gencode.v47.lncRNA_transcripts.fa.gz"
    index_loc = "/lustre/work/stexocae/li_lab/refs/hg38/star/"
else:
    print("Build must be hg38 or chm13")

sample_loc = working_dir + "sim/" + sample + "/" + sample
sample_list = working_dir + "tespex/" + sample + "_input.txt"
out_loc = working_dir + "/tespex/" + sample
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/tespex.py"


## directory ##
#mkdir_call = "mkdir " + out_loc
#subprocess.run(mkdir_call, shell=True)

## make sample input file ##
with open(sample_list, "w") as f:
    samples =  sample_loc+ "_1.fastq\t" + sample_loc + "_2.fastq"
    f.write(samples)


tespex_call = "python3 " + tespex_loc + " --TE " + te_loc + " "
tespex_call += "--cdna " + cdna_loc + " --ncrna " + ncrna_loc + " "
tespex_call += "--sample " + sample_list + " --paired T --length 100 " 
tespex_call += "--out " + out_loc + " --strand yes "
tespex_call += "--num_threads 32 --remove T "

print(tespex_call)
subprocess.run(tespex_call, shell=True)


## translate_call ##
translate_call = "python3 " + translate_loc + " " + build + " " + gtf + " " + sample + " " + n_de + " " + depth
subprocess.run(translate_call, shell=True)

## clean up ##
#rm_call = "rm -rf " + out_loc + "*"
#subprocess.run(rm_call, shell=True)
