import sys
import subprocess

srr = sys.argv[1]


package_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/LIONS/"
folder_loc = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/lions/"
sample_loc = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/" + srr
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/lions.gtf"
software_loc = package_loc + "software/"
sys_template_loc = package_loc + "controls/template/system.sysctrl"
template_loc = package_loc + "controls/template/parameter.ctrl"
input_loc = folder_loc + "controls/input.ctrl"
params_loc = folder_loc + "controls/params.ctrl"
sys_params_loc = folder_loc + "controls/system.ctrl"

## make input_list ##
mkdir_call = "mkdir " + folder_loc
mkdir2_call = "mkdir " + folder_loc + "controls"
input_list = srr + "\t" + sample_loc + "_1.fastq," + sample_loc + "_2.fastq\t1"
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
            l = split(l) + "'" + srr + "'\n"
        if "INPUT_LIST=" in l:
            l = split(l) + '"' + input_loc + '"\n'
        if "INDEX=" in l:
            l = split(l) + "'chm13'\n"
        if "GENESET=" in l:
            l = split(l) + "'refseq_chm13.ucsc'\n"
        if "REPEATMASKER=" in l:
            l = split(l) + "'rm_chm13.ucsc'\n"
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
raw_counts_loc = folder_loc + srr + "_1.lcsv"
final_counts_loc = folder_loc + "final_counts.csv"
out_bed_loc = folder_loc + srr + ".bed"
bedtools_out_loc = folder_loc + srr + ".bedtools.out"
out_bed = []
out_csv = []

with open(raw_counts_loc, "r") as f:
    lines = f.readlines()[1:]
    for line in lines:
        buff = line.strip().split()
        buff2 = buff[3].replace(":", " ").replace("-", " ").split()
        out_bed += [buff2 + [str(int(float(buff[30])))]]
with open(out_bed_loc, "w") as f:
    for line in out_bed:
        f.write("\t".join(line) + "\n")
bedtools_call = "bedtools intersect -wo -a " + out_bed_loc + " -b " + gtf_loc + " -f .25 -r > " + bedtools_out_loc
subprocess.run(bedtools_call, shell=True)

with open(bedtools_out_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        out_csv += [[buff[15][1:-2], buff[3]]]



with open(final_counts_loc, "w") as f:
    for line in out_csv:
        f.write(line[0] + "," + line[1] + "\n")
