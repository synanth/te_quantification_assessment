import subprocess
import sys

build = sys.argv[1]
gtf = sys.argv[2]
n_samples = sys.argv[3]
depth = sys.argv[4]

slurm_loc = "/home/stexocae/li_lab/te_sim/scripts/slurm/"
methods = ["ervmap", "explorate", "squire", "tecount", "telescope", "telocal", "tespex", "tetools", "texp"]


base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_samples + "_" + depth + "/"
star_loc = base_loc + "star/"
bowtie2_loc = base_loc + "bowtie2/"
samples_loc = base_loc + "sim/"


for x in range(1, 2*(int(n_samples))+1):
    ## move to sample folder ##
    mv_call = "mv " + base_loc + "sample_" + str(x).zfill(2) + "* " + samples_loc + "sample_" + str(x).zfill(2) + "/"
    subprocess.run(mv_call, shell=True)

    ## make fastq from fasta ##
    sample_loc = samples_loc + "sample_" + str(x).zfill(2) + "/sample_" + str(x).zfill(2) 
    seqtk_call_1 = "seqtk seq -F 'I' " + sample_loc + "_1.fasta > " + sample_loc + "_R1.fq"
    seqtk_call_2 = "seqtk seq -F 'I' " + sample_loc + "_2.fasta > " + sample_loc + "_R2.fq"
    subprocess.run(seqtk_call_1, shell=True)
    subprocess.run(seqtk_call_2, shell=True)

    ## copy .fq to fastq ##
    cp_call_1 = "cp " + sample_loc + "_R1.fq " + sample_loc + "_1.fastq"
    cp_call_2 = "cp " + sample_loc + "_R2.fq " + sample_loc + "_2.fastq"
    subprocess.run(cp_call_1, shell=True)
    subprocess.run(cp_call_2, shell=True)

## move simulation metadata ##
mv_call_2 = "mv " + base_loc + "sim_* " + samples_loc
subprocess.run(mv_call_2, shell=True)
