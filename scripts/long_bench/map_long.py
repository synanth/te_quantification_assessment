import subprocess
import sys

srr = sys.argv[1]

base_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
fastq_loc = base_dir + srr + ".fastq"
aln_loc = base_dir + "long.bam"
genome_loc = "/home/stexocae/li_lab/saem/refs/hs1.mmi"

minimap_call = "minimap2 -ax splice:hq --secondary=no -t 16 " + genome_loc + " " + fastq_loc + " > " + aln_loc

subprocess.call(minimap_call, shell=True)
