## This program runs ERVmap

import sys
import subprocess


## parameters ##
srr = sys.argv[1]

## set up dirs ##
working_dir = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/"
ervmap_base_loc = "/home/stexocae/li_lab/te_sim/scripts/quant/packages/ERVmap/"
ref_base_loc = "/lustre/work/stexocae/li_lab/refs/"

in_bwa = ref_base_loc + "chm13/erv_map/chm13"
in_bowtie = ref_base_loc + "chm13/bowtie2/chm13"
in_bed = ref_base_loc + "te_annotations/bed/ervmap_chm13.bed"
in_len = ervmap_base_loc + "ref/hs1.chrom.sizes.txt"
in_gtf = ref_base_loc + "chm13/raw/chm13.gtf"
in_transcriptome = ervmap_base_loc + "ref/"


in_adaptor = ervmap_base_loc + "ref/illumina_adapter.txt"
in_filter = ervmap_base_loc + "scripts/parse_bam.pl"
ervmap_data_loc = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/ervmap/"
out_loc = "/lustre/research/dawli/stexocaelum/longbench/" + srr + "/ervmap/"
in_fastq = out_loc + srr + ".fastq"

mkdir_call = "mkdir " + out_loc
subprocess.run(mkdir_call, shell=True)


## combine fastas ##
interleave_call = "perl " + ervmap_base_loc + "scripts/interleaved.pl --read1 "
interleave_call += working_dir + srr + "_1.fastq --read2 "
interleave_call += working_dir + srr + "_2.fastq > "
interleave_call += out_loc + srr + ".fastq"
cp_call = "cp " + out_loc + srr + ".fastq " + out_loc + "btrim_g_se.out"


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


## translate to csv ##
raw_loc = out_loc + "herv_coverage_GRCh38_genome.txt"
final_counts_loc = out_loc + "final_counts.csv"
out_csv = []


with open(raw_loc, "r") as f:
    lines = f.readlines()
    for line in lines:
        buff = line.strip().split()
        out_csv += [[buff[3], buff[6]]]

with open(final_counts_loc, "w") as f:
    for line in out_csv:
        f.write(line[0] + "," + line[1] + "\n")
