import sys
import subprocess

srr = sys.argv[1]

working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"

program_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/ExplorATE_shell_script/ExplorATE"
ref_path = "/lustre/work/stexocae/li_lab/refs/"
conda_path = "/home/stexocae/miniconda3/envs/explorate/bin/"
bedtools_loc = conda_path + "bedtools"
salmon_loc = conda_path + "salmon"

fa_loc = ref_path + "chm13/raw/chm13.fa"
gtf_loc = ref_path + "chm13/raw/chm13.gtf"
rmsk_loc = ref_path + "chm13/raw/rmsk.out"
te_loc = ref_path + "te_annotations/hammell/chm13.fa"


sample_loc = working_dir 
out_loc = working_dir + "explorate/"
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/explorate.py"

cp_call1 = "cp " + working_dir + srr + "_1.fastq " + out_loc + "reads/" + srr + "_R1.fq"
cp_call2 = "cp " + working_dir + srr + "_2.fastq " + out_loc + "reads/" + srr + "_R2.fq"

subprocess.run("mkdir " + out_loc, shell=True)
subprocess.run("mkdir " + out_loc + "reads", shell=True)
subprocess.run(cp_call1, shell=True)
subprocess.run(cp_call2, shell=True)


explorate_call = "bash " + program_loc + " mo -p16 -b " + bedtools_loc + " "
explorate_call += "-s " + salmon_loc + " -f " + fa_loc + " -g " + gtf_loc + " "
explorate_call += "-r " + rmsk_loc + " -e pe -l " + out_loc + "reads/ "
explorate_call += "-o " + out_loc


print(explorate_call)
subprocess.run(explorate_call, shell=True)

## translate ##
raw_counts_loc = out_loc + "quant_out/" + srr + "/quant.sf"
out_csv_loc = out_loc + "final_counts.csv"
out_csv = []

with open(raw_counts_loc, "r") as f:
    lines = f.readlines()[1:]
    for line in lines:
        buff = line.strip().split()
        out_csv += [[buff[0], str(round(float(buff[-1])))]]
with open(out_csv_loc, "w") as f:
    for line in out_csv:
        f.write(line[0] + "," + line[1] + "\n")
