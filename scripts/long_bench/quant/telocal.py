import sys
import subprocess

srr = sys.argv[1]

working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
sample_loc = working_dir + "star.bam"
out_loc = working_dir + "telocal/" 


gene_gtf_loc = "/lustre/work/stexocae/li_lab/refs/chm13/raw/chm13.gtf"
te_gtf_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/hammell/chm13.locInd"
mkdir_call = "mkdir " + out_loc

telocal_call = "TElocal --stranded forward "
telocal_call += "-b " + sample_loc + " "
telocal_call += "--GTF " + gene_gtf_loc + " "
telocal_call += "--TE " + te_gtf_loc + " "
telocal_call += "--project " + out_loc


#subprocess.run(mkdir_call, shell=True)
#subprocess.run(telocal_call, shell=True)

## translate ##
raw_counts_loc = out_loc + ".cntTable"
final_counts_loc = out_loc + "final_counts.csv"
out_csv = []

with open(raw_counts_loc, "r") as f:
    lines = f.readlines()[1:]
    for line in lines:
        buff = line.strip().split()
        if buff[0][0] == '"':
            continue
        name = buff[0].split(":")[0]
        out_csv += [[name, buff[1]]]
with open(final_counts_loc, "w") as f:
    for line in out_csv:
        f.write(line[0] + "," + line[1] + "\n")
