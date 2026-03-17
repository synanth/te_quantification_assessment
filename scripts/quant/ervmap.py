## This program runs ERVmap

import sys
import subprocess


## parameters ##
build = sys.argv[1]
gtf = sys.argv[2]
sample = sys.argv[3]
n_samples = sys.argv[4]
depth = sys.argv[5]


## set up dirs ##
working_dir = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_samples + "_" + depth + "/sim/" + sample + "/"
ervmap_base_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/ERVmap/"
ref_base_loc = "/lustre/work/stexocae/li_lab/refs/"

if build == "chm13":
    in_bwa = ref_base_loc + "chm13/erv_map/chm13"
    in_bowtie = ref_base_loc + "chm13/bowtie2/chm13"
    in_bed = ref_base_loc + "te_annotations/bed/ervmap_chm13.bed"
    in_len = ervmap_base_loc + "ref/hs1.chrom.sizes.txt"
    in_gtf = ref_base_loc + "chm13/raw/chm13.gtf"
    in_transcriptome = ervmap_base_loc + "ref/"
elif build == "hg38":
    in_bwa = ref_base_loc + "hg38/erv_map/hg38"
    in_bowtie = ref_base_loc + "hg38/bowtie2/hg38"
    in_bed = ref_base_loc + "te_annotations/bed/ervmap_hg38.bed"
    in_len = ervmap_base_loc + "ref/GRCh38.genome_file.txt"
    in_gtf = ref_base_loc + "hg38/raw/hg38.gtf"
    in_transcriptome = ervmap_base_loc + "ref/"
else:
    sys.exit("Build should be hg38 or chm13")

in_adaptor = ervmap_base_loc + "ref/illumina_adapter.txt"
in_filter = ervmap_base_loc + "scripts/parse_bam.pl"
ervmap_data_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_samples + "_" + depth + "/ervmap/"
out_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + build + "_" + gtf + "_" + n_samples + "_" + depth + "/ervmap/" + sample + "/"
in_fastq = out_loc + sample + ".fasta"
translate_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/helpers/translate/ervmap.py"

mkdir_call = "mkdir " + out_loc
subprocess.run(mkdir_call, shell=True)


## combine fastas ##
interleave_call = "perl " + ervmap_base_loc + "scripts/interleaved.pl --read1 "
interleave_call += working_dir + sample + "_1.fasta --read2 "
interleave_call += working_dir + sample + "_2.fasta > "
interleave_call += out_loc + sample + ".fasta"
cp_call = "cp " + out_loc + sample + ".fasta " + out_loc + "btrim_g_se.out"

print(interleave_call)

subprocess.run(interleave_call, shell=True)
subprocess.run(cp_call, shell=True)

## ervmap call ##
ervmap_call = "perl " + ervmap_base_loc + "scripts/erv_genome.pl "
ervmap_call += "-start_stage 2 -end_stage 4 " 
ervmap_call += "--fastq " + in_fastq + " "
ervmap_call += "--genome " + in_bwa + " "
ervmap_call += "--genome_Bowtie2 " + in_bowtie + " "
ervmap_call += "--bed " + in_bed + " " 
ervmap_call += "--genomefile " + in_len + " "
ervmap_call += "--gtf " + in_gtf + " " 
ervmap_call += "--transcriptome " + in_transcriptome + " " 
ervmap_call += "--adaptor " + in_adaptor + " " 
ervmap_call += "--filter " + in_filter + " " 
ervmap_call += "--cell " + out_loc

subprocess.run(ervmap_call, shell=True)


## translate coordinates ##
translate_call = "python3 " + translate_loc + " " + build + " " + gtf + " " + sample + " " + n_samples + " " + depth
subprocess.run(translate_call, shell=True)


## clean up ##
#rm_call = "rm -rf " + out_loc
#subprocess.run(rm_call, shell=True)
