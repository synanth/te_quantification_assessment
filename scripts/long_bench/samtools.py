import sys
import subprocess

lr_id = sys.argv[1]
data_loc = "/lustre/research/dawli/stexocaelum/longbench/" + lr_id + "/long.bam"
out_loc = "/lustre/research/dawli/stexocaelum/longbench/" + lr_id + "/filtered.bam"

samtools_call = "samtools view -F 260 -q 20 -o " + out_loc + " " + data_loc
subprocess.run(samtools_call, shell=True)
