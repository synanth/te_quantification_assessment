import os
import sys
import subprocess

## file mgmt ##
build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_samples = sys.argv[4]
depth= sys.argv[5]

num_cpu = str(os.cpu_count() -1)
working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_samples + "_" + depth + "/" 

if build == "chm13":
    ref_file = "/lustre/work/stexocae/li_lab/refs/chm13/bowtie2/chm13"
elif build == "hg38":
    ref_file = "/lustre/work/stexocae/li_lab/refs/hg38/bowtie2/hg38"
else:
    print("Build must be hg38 or chm13")
    quit()

out_dir = working_dir + "bowtie2/"
fa_dir = working_dir + "sim/" + sample + "/" 
bam_loc = fa_dir + "bowtie2.bam"


## bowtie2 call ##
bowtie2_call = "bowtie2 -k 100 --very-sensitive-local --score-min 'L,0,1.6' "
bowtie2_call += "-p " + num_cpu + " "
bowtie2_call += "-x " + ref_file + " -f "
bowtie2_call += "-1 " + fa_dir + sample + "_1.fasta "
bowtie2_call += "-2 " + fa_dir + sample + "_2.fasta "
bowtie2_call += "--rg-id " + sample + " | samtools view -bS - > " + bam_loc


## run subprocesses ##
subprocess.call(bowtie2_call, shell=True)
