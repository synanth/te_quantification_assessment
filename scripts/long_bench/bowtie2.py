import os
import sys
import subprocess

srr = sys.argv[1]

num_cpu = str(16)
working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/" 
ref_file = "/lustre/work/stexocae/li_lab/refs/chm13/bowtie2/chm13"

out_dir = working_dir + "bowtie2/"
fa_dir = working_dir + srr
bam_loc = working_dir + "bowtie2.bam"


## bowtie2 call ##
bowtie2_call = "bowtie2 -k 100 --very-sensitive-local --score-min 'L,0,1.6' "
bowtie2_call += "-p " + num_cpu + " "
bowtie2_call += "-x " + ref_file + " "
bowtie2_call += "-1 " + fa_dir + "_1.fastq "
bowtie2_call += "-2 " + fa_dir + "_2.fastq "
bowtie2_call += "--rg-id " + srr + " | samtools view -bS - > " + bam_loc


## run subprocesses ##
subprocess.call(bowtie2_call, shell=True)
