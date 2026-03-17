import subprocess
import sys

srr = sys.argv[1]
method = sys.argv[2]

base_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
aln_loc = base_dir + "filtered.bam"
out_loc = base_dir + "fc_" + method + ".out"
gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/" + method + ".gtf"

if method == "telescope":
    fc_call = "featureCounts -O -t gene -L --primary -T 16 -f -g transcript_id -a " + gtf_loc + " -o " + out_loc + " " + aln_loc
else:
    fc_call = "featureCounts -O -L --primary -T 16 -f -g transcript_id -a " + gtf_loc + " -o " + out_loc + " " + aln_loc

subprocess.call(fc_call, shell=True)
