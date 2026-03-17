import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_de = sys.argv[4]
depth = sys.argv[5]

working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/"
sample_loc = working_dir + "sim/" + sample + "/star.bam"

if build == "chm13":
    gene_gtf_loc = "/lustre/work/stexocae/li_lab/refs/chm13/raw/chm13.gtf"
    te_gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/hammell/chm13.gtf"
elif build == "hg38":
    gene_gtf_loc = "/lustre/work/stexocae/li_lab/refs/hg38/raw/hg38.gtf"
    te_gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/hammell/hg38.gtf"
else:
    print("Build must be hg38 or chm13")
    quit()

out_dir = working_dir + "tecount/" + sample
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/tecount.py"

mkdir_call = "mkdir " + out_dir

tecount_call = "TEcount --stranded forward "
tecount_call += "-b " + sample_loc + " "
tecount_call += "--GTF " + gene_gtf_loc + " "
tecount_call += "--TE " + te_gtf_loc + " "
tecount_call += "--outdir " + out_dir


subprocess.run(mkdir_call, shell=True)
subprocess.run(tecount_call, shell=True)


## translate ##
translate_call = "python3 " + translate_loc + " " + build + " " + gtf + " " + sample + " " + n_de + " " + depth
subprocess.run(translate_call, shell=True)


## clean up ##
#rm_call = "rm -rf " + out_dir
#subprocess.run(rm_call, shell=True)
