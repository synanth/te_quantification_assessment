import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_de = sys.argv[4]
depth = sys.argv[5]

working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/"
program_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/ExplorATE_shell_script/ExplorATE"
ref_path = "/lustre/work/stexocae/li_lab/refs/"
conda_path = "/home/stexocae/miniconda3/envs/explorate/bin/"
bedtools_loc = conda_path + "bedtools"
salmon_loc = conda_path + "salmon"

if build == "chm13":
    fa_loc = ref_path + "chm13/raw/chm13.fa"
    gtf_loc = ref_path + "chm13/raw/chm13.gtf"
    rmsk_loc = ref_path + "chm13/raw/rmsk.out"
    te_loc = ref_path + "te_annotations/hammell/chm13.fa"
elif build == "hg38":
    fa_loc = ref_path + "hg38/raw/hg38.fa"
    gtf_loc = ref_path + "hg38/raw/hg38.gtf"
    rmsk_loc = ref_path + "hg38/raw/rmsk.out"
    te_loc = ref_path + "te_annotations/hammell/hg38.fa"
else:
    sys.exit("Only hg38 or chm13 work for now")

sample_loc = working_dir + "sim/" + sample + "/"
out_loc = working_dir + "explorate/" + sample + "/"
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/explorate.py"

mkdir_call = "mkdir " + out_loc

explorate_call = "bash " + program_loc + " mo -p12 -b " + bedtools_loc + " "
explorate_call += "-s " + salmon_loc + " -f " + fa_loc + " -g " + gtf_loc + " "
explorate_call += "-r " + rmsk_loc + " -e pe -l " + sample_loc + " "
explorate_call += "-o " + out_loc


print(explorate_call)
subprocess.run(mkdir_call, shell=True)
subprocess.run(explorate_call, shell=True)


## translate ##
translate_call = "python3 " + translate_loc + " " + build + " " + gtf + " " + sample + " " + n_de + " " + depth
subprocess.run(translate_call, shell=True)

## clean up ##
#rm_call = "rm -rf " + out_loc
#subprocess.run(rm_call, shell=True)
