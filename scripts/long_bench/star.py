import os
import sys
import subprocess

srr = sys.argv[1]

num_cpu = str(os.cpu_count() -1)

working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
sample_loc = working_dir + srr
ref_dir = "/lustre/work/stexocae/li_lab/refs/chm13/star/"


out_loc = working_dir + "star"

star_call = "STAR --runThreadN " + num_cpu + " --genomeDir " + ref_dir 
star_call += " --outFilterMultimapNmax 100 --winAnchorMultimapNmax 100"
star_call += " --outFileNamePrefix " + out_loc + "_"
star_call += " --outSAMtype BAM Unsorted "
star_call += " --readFilesIn " + sample_loc + "_1.fastq " + sample_loc + "_2.fastq"

subprocess.call(star_call, shell=True)
sort_call = "samtools sort " + out_loc + "_Aligned.out.bam -o " + out_loc + "_sorted.sam" 
subprocess.call(sort_call, shell=True)


## clean up
mv_call = "mv " + out_loc + "_Aligned.out.bam " + out_loc + ".bam"
rm_call1 = "rm " + out_loc + "_Log.final.out"
rm_call2 = "rm " + out_loc + "_Log.out"
rm_call3 = "rm " + out_loc + "_Log.progress.out"
rm_call4 = "rm " + out_loc + "_SJ.out.tab"



subprocess.call(mv_call, shell=True)
subprocess.call(rm_call1, shell=True)
subprocess.call(rm_call2, shell=True)
subprocess.call(rm_call3, shell=True)
subprocess.call(rm_call4, shell=True)
