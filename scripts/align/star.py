import os
import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_de = sys.argv[4]
depth = sys.argv[5]

num_cpu = str(os.cpu_count() -1)

working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_de + "_" + depth + "/"
sample_loc = working_dir + "sim/" + sample + "/"

if build == "chm13":
    ref_dir = "/lustre/work/stexocae/li_lab/refs/chm13/star/"
elif build == "hg38":
    ref_dir = "/lustre/work/stexocae/li_lab/refs/hg38/star/"
else:
    sys.exit("Build must be hg38 or chm13")

out_loc = sample_loc + "star"

star_call = "STAR --runThreadN " + num_cpu + " --genomeDir " + ref_dir 
star_call += " --outFilterMultimapNmax 100 --winAnchorMultimapNmax 100"
star_call += " --outFileNamePrefix " + out_loc + "_"
star_call += " --outSAMtype BAM Unsorted "
star_call += " --readFilesIn " + sample_loc + sample + "_1.fasta " + sample_loc + sample + "_2.fasta"

subprocess.call(star_call, shell=True)
print(star_call)
sort_call = "samtools sort " + out_loc + "_Aligned.out.bam -o " + out_loc + "_sorted.sam" 
subprocess.call(sort_call, shell=True)


## clean up
#rm_log_call = "rm " + out_loc + "_Log.*"
#rm_sj_call = "rm " + out_loc + "_SJ.out.tab"
mv_call = "mv " + out_loc + "_Aligned.out.bam " + out_loc + ".bam"


#print(rm_log_call)
print(mv_call)
#subprocess.call(rm_log_call, shell=True)
#subprocess.call(rm_sj_call, shell=True)
subprocess.call(mv_call, shell=True)
