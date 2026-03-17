import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_reps = sys.argv[4]
depth = sys.argv[5]


package_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/LIONS/"
folder_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/lions/" + sample + "/"
sample_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/" + sample + "/" + sample
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/" + gtf + ".gtf"
software_loc = package_loc + "software/"
sys_template_loc = package_loc + "controls/template/system.sysctrl"
template_loc = package_loc + "controls/template/parameter.ctrl"
input_loc = folder_loc + "controls/input.ctrl"
params_loc = folder_loc + "controls/params.ctrl"
sys_params_loc = folder_loc + "controls/system.ctrl"
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/lions.py"

## make input_list ##
mkdir_call = "mkdir " + folder_loc
mkdir2_call = "mkdir " + folder_loc + "controls"
input_list = sample + "\t" + sample_loc + "_R1.fq," + sample_loc + "_R2.fq\t1"
subprocess.run(mkdir_call, shell=True)
subprocess.run(mkdir2_call, shell=True)
with open(input_loc, "w") as f:
    f.write(input_list)

## populate params ##
sys_params = []
params = []

def split(s):
    s = s.split("=")
    s = s[0] + "="
    return s

with open(sys_template_loc, "r") as f:
    lines = f.readlines()
    for l in lines:
        if "pDIR=" in l:
            l = split(l) + '"' + folder_loc[:-1] + '"\n'
        if "THREADS=" in l:
            l = split(l) + "'8'\n" 
        if "SAMTOOLS=" in l:
            l = split(l) + "'" + software_loc + "samtools-0.1.19/samtools'\n"
        if "BAM2FASTX=" in l:
            l = split(l) + "'" + software_loc + "tophat-2.1.1.Linux_x86_64/bam2fastx'\n"
        if "TOPHAT2=" in l:
            l = split(l) + "'" + software_loc + "tophat-2.1.1.Linux_x86_64/tophat2'\n"
        if "CUFFLINKS=" in l:
            l = split(l) + "'" + software_loc + "cufflinks-2.2.1.Linux_x86_64/cufflinks'\n"
        if "BOWTIE_BUILD=" in l:
            l = split(l) + "'bowtie2-build'\n"
        sys_params += l

with open(sys_params_loc, "w") as f:
    for x in sys_params:
        f.write(x)


with open(template_loc, "r") as f:
    lines = f.readlines()
    for l in lines:
        if "BASE=" in l:
            l = split(l) + '"' + package_loc[:-1] + '"\n'
        if "PROJECT=" in l:
            l = split(l) + "'" + gtf + "_" + n_reps + "_" + depth + "'\n"
        if "INPUT_LIST=" in l:
            l = split(l) + '"' + input_loc + '"\n'
        if "INDEX=" in l:
            if build == "chm13":
                l = split(l) + "'chm13'\n"
            if build == "hg38":
                l = split(l) + "'hg38'\n"
        if "GENESET=" in l:
            if build == "chm13":
                l = split(l) + "'refseq_chm13.ucsc'\n"
            elif build == "hg38":
                l = split(l) + "'refseq_hg38.ucsc'\n"
        if "REPEATMASKER=" in l:
            if build == "chm13":
                l = split(l) + "'rm_chm13.ucsc'\n"
            elif build == "hg38":
                l = split(l) + "'rm_hg38.ucsc'\n"
        if "SYSTEMCTRL=" in l:
            l = split(l) + '"' + sys_params_loc + '"\n'
        if "ALIGNBYPASS=" in l:
            l = split(l) + "'1'\n"
        if "deNovo=" in l:
            l = split(l) + "'1'\n"
        if "guide=" in l:
            l = split(l) + '"' + gtf_loc + '"\n'
        params += l

with open(params_loc, "w") as f:
    for x in params:
        f.write(x)

## call script ##
script_loc = package_loc + "lions.sh"

lions_call = "cd " + package_loc + " && " + script_loc + " " + params_loc

print(lions_call)
subprocess.run(lions_call, shell=True)


## translate ##
translate_call = "python3 " + translate_loc + " " + build + " " + gtf + " " + sample + " " + n_reps + " " + depth
subprocess.run(translate_call, shell = True)

## clean up ##
#clean_call = "rm -rf " + folder_loc
#subprocess.run(clean_call, shell=True)
