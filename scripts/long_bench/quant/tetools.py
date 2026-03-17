import sys
import subprocess

srr = sys.argv[1]

working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
program_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/TEtools/TEcount.py"

rosette_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/tetools/chm13.txt"
te_loc = "/lustre/work/stexocae/li_lab/refs/te_annotations/tetools/chm13.fa"

sam_loc = working_dir + "star_sorted.sam"
fasta_loc1 = working_dir + srr + "_1.fastq"
fasta_loc2 = working_dir + srr + "_2.fastq"
out_loc = working_dir + "tetools/" + srr
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/tetools.py"

subprocess.run("mkdir " + working_dir + "tetools", shell=True)

## copy te and rosette loc to working folder ##
cp1_call = "cp " + te_loc + " " + out_loc
cp2_call = "cp " + rosette_loc + " " + out_loc
subprocess.run(cp1_call, shell=True)
subprocess.run(cp2_call, shell=True)





tetools_call = "python " + program_loc + " -rosette=" + rosette_loc + " "
tetools_call += "-column=2 -TE_fasta=" + te_loc + " "
tetools_call += "-count=" + out_loc + " "
tetools_call += " -RNA=" + fasta_loc1 + " " 
tetools_call += "-RNApair=" + fasta_loc2

subprocess.run(tetools_call, shell=True)

## translate ##
raw_counts_loc = working_dir + "tetools/" + srr
final_counts_loc = working_dir + "tetools/final_counts.csv"
out_csv = []

with open(raw_counts_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        out_csv += [[buff[0], buff[2]]]

with open(final_counts_loc, "w") as f:
    for line in out_csv:
        f.write(line[0] + "," + line[1] + "\n")
