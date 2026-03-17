import sys
import subprocess

srr = sys.argv[1]

working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
te_gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/bendall/chm13.gtf"
sample_loc = working_dir + "bowtie2.bam"
    

telescope_call = "telescope assign --theta_prior 200000 --max_iter 200 --outdir "
telescope_call += working_dir + "telescope/ " + sample_loc + " " + te_gtf_loc + " 2>&1 | tee " + working_dir + "telescope/" + srr + ".log"


mkdir_call = "mkdir " + working_dir + "telescope"
subprocess.run(mkdir_call, shell=True)
subprocess.run(telescope_call, shell=True)

## translate ##
raw_counts_loc = working_dir + "telescope/telescope-telescope_report.tsv"
final_counts_loc = working_dir + "telescope/final_counts.csv"
out_csv = []

with open(raw_counts_loc, "r") as f:
    lines = f.readlines()[2:]
    for line in lines:
        buff = line.strip().split()
        if buff[0] == "__no_feature":
            continue
        out_csv += [[buff[0], buff[2]]]

with open(final_counts_loc, "w") as f:
    for line in out_csv:
        f.write(line[0] + "," + line[1] + "\n")
