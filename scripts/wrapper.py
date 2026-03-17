## This acts as the main function for TE Quantification simulation assessments

import subprocess
import random
import sys
import os

## parameters ##
build = sys.argv[1]
gtf = sys.argv[2]
n_samples = sys.argv[3]
depth = sys.argv[4]

slurm_loc = "/home/stexocae/li_lab/te_sim/scripts/slurm/"
methods = ["ervmap", "explorate", "lions", "squire", "telescope", "telocal", "te-saem", "tetools", "texp"]


## pretty printing ##
print("\n#############################################")
print("### RNA-Seq TE Quantification Assessments ###")
print("#############################################\n")
print("Number Replicates: " + n_samples)
print("GTF: " + gtf)
print("Depth: " + depth)
print("\n#############################################\n")


## make directory structure ##
home_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/"
base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_samples + "_" + depth + "/"
samples_loc = base_loc + "sim/"
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/" + build + "/" + gtf + ".gtf"
subset_loc = samples_loc + "subset.gtf"
len_loc = samples_loc + "subset.len"

subprocess.run("mkdir " + base_loc, shell=True)
subprocess.run("mkdir " + samples_loc, shell=True)
for x in methods:
    subprocess.run("mkdir " + base_loc + x, shell=True)
for x in range(1, 2*(int(n_samples))+1):
    sample_loc = samples_loc + "sample_" + str(x).zfill(2)
    subprocess.run("mkdir " + sample_loc, shell=True)

mkdir_call = "mkdir " + samples_loc + "assess/"
subprocess.run(mkdir_call, shell=True)
mkdir_call = "mkdir " + base_loc + "viz/"
subprocess.run(mkdir_call, shell=True)

for method in methods:
    mk_complexity_call = "touch " + samples_loc + "assess/complexity_" + method + ".csv"
    subprocess.run(mk_complexity_call, shell=True)

mk_complexity_call = "touch " + samples_loc + "assess/complexity_bowtie2.csv"
subprocess.run(mk_complexity_call, shell=True)
mk_complexity_call = "touch " + samples_loc + "assess/complexity_star.csv"
subprocess.run(mk_complexity_call, shell=True)

os.chdir(base_loc)


## choose gtf subset ##
with open(gtf_loc, "r") as f:
    lines = f.readlines()       
if len(lines) > 50000:
    gtf_subset = random.sample(lines, 50000)
else:
    gtf_subset = lines
lens = []
with open(subset_loc, "w") as f:
    for x in gtf_subset:
        f.write(x)
        buff = x.strip().split()
        lens += [int(buff[4]) - int(buff[3])]
with open(len_loc, "w") as f:
    for x in lens:
        f.write(str(x) + "\n")


## simulate ##
print("Simulating data:")
sim_loc = slurm_loc + "sim.sh"
sim_call = "bash " + sim_loc + " " + build + " " + gtf + " " + n_samples + " " + depth

output = subprocess.run(sim_call, shell=True,stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()
sim_jobid = output[-1]
print("\t" + sim_call)
mv_call = "bash " + slurm_loc + "mv_call.sh " + build + " " + gtf + " " + n_samples + " " + depth + " " + sim_jobid
output = subprocess.run(mv_call, shell=True,stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()
mv_jobid = output[-1]
print("\t" + mv_call)


## align ##
print("\nAligning data:")
bowtie2_loc = slurm_loc + "bowtie2.sh"
star_loc = slurm_loc + "star.sh"
align_jobid = ""

for x in range(1, 2*(int(n_samples)) + 1):
    print("\tSample " + str(x).zfill(2) + ":")
    bowtie2_call = "bash " + bowtie2_loc + " " + build + " " + gtf + " sample_" + str(x).zfill(2) + " " + n_samples + " " + depth + " " + mv_jobid
    star_call = "bash " + star_loc + " " + build + " " + gtf + " sample_" + str(x).zfill(2) + " " + n_samples + " " + depth + " " + mv_jobid
    print("\t\t" + bowtie2_call)
    print("\t\t" + star_call)
    bowtie2_output = subprocess.run(bowtie2_call, shell=True,stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()
    star_output = subprocess.run(star_call, shell=True,stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()
    complexity_call = "bash " + slurm_loc + "complexity.sh " + bowtie2_output[-1]
    subprocess.run(complexity_call, shell=True)
    complexity_call = "bash " + slurm_loc + "complexity.sh " + star_output[-1]
    subprocess.run(complexity_call, shell=True)

    align_jobid += bowtie2_output[-1] + "," + star_output[-1] + ","
    
align_jobid = align_jobid[:-1]


## quantify TEs ##
print("\nQuantifying TEs:")

for x in range(1, 2*(int(n_samples)) + 1):
    mkdir_call = "mkdir " + samples_loc + "sample_" + str(x).zfill(2) + "/counts/"
    subprocess.run(mkdir_call, shell=True)
matrix_jobids = []

for y in methods:
    quant_jobid = ""
    matrix_jobid = ""
    for x in range(1, 2*(int(n_samples)) + 1):
        method_loc = slurm_loc + y + ".sh"
        quant_call = "bash " + method_loc + " " + build + " " + gtf + " sample_" + str(x).zfill(2) + " " + n_samples + " " + depth + " " + align_jobid
        print("\t\t" + quant_call) 
        quant_output = subprocess.run(quant_call, shell=True,stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()
        quant_jobid += quant_output[-1] + ","
        ## complexity ##
        complexity_call = "bash " + slurm_loc + "complexity.sh " + quant_output[-1]
        subprocess.run(complexity_call, shell=True)
    quant_jobid = quant_jobid[:-1]

    ## make matrices ##
    matrix_call = "bash " + slurm_loc + "matrix.sh " + build + " " + gtf + " " + y + " " + n_samples + " " + depth + " " + quant_jobid
    print("\t\t" + matrix_call)
    matrix_output = subprocess.run(matrix_call, shell=True,stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()
    matrix_jobids += [matrix_output[-1]]
matrix_jobids = ",".join(matrix_jobids)
print(matrix_jobids)


## assessments ##
print("\nPerforming assessments:")

raw_assess_loc = slurm_loc + "raw_assess.sh"
deseq_assess_loc = slurm_loc + "deseq_assess.sh"
family_assess_loc = slurm_loc + "family_assess.sh"

family_assess_call = "bash " + family_assess_loc + " " + build + " " + gtf + " " + n_samples + " " + depth + " " + matrix_jobids
subprocess.run(family_assess_call, shell=True)

raw_jobids = ""
deseq_jobids = ""
for y in methods:
    raw_call = "bash " + raw_assess_loc + " " + build + " " + gtf + " " + y + " " + n_samples + " " + depth + " " + matrix_jobids
    print("\t\t" + raw_call) 
    raw_output = subprocess.run(raw_call, shell=True,stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()
    raw_jobids += raw_output[-1] + ","


## clean up ##
jobids = deseq_jobids + raw_jobids
jobids = jobids[:-1]
print("\nCleaning file structure:")
clean_call = "bash " + slurm_loc + "cleanup.sh " + build + " " + gtf  + " " + n_samples + " " + depth + " " + jobids
print(clean_call)
subprocess.run(clean_call, shell=True)

print("\nfin.\n")
