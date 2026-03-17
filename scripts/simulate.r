## This program simulates RNA-Seq data for TE quantification software analysis.

library("polyester")
library("Biostrings")

## parameters ##
args = commandArgs(trailingOnly=TRUE)
build <- args[[1]]
gtf_type <- args[[2]]
num_reps <- as.integer(args[[3]])
depth <- as.integer(args[[4]])
num_deg <- 1000


## data management ##
if (build == "chm13"){
    fasta_loc <- "/lustre/work/stexocae/li_lab/refs/chm13/raw/chromosomes"
} else if (build == "hg38"){
    fasta_loc <- "/lustre/work/stexocae/li_lab/refs/hg38/raw/chromosomes"
}

sim_loc <- paste0("/lustre/research/dawli/stexocaelum/TE_quantification_simulation/", build, "_", gtf_type, "_", num_reps, "_", depth, "/")
#sim_loc <- "/home/stexocae/li_lab/saem/refs/"
gtf_loc <- paste0(sim_loc, "sim/subset.gtf")
#gtf_loc <- paste0(sim_loc, "subset.gtf")
len_loc <- paste0(sim_loc, "sim/subset.len")
#len_loc <- paste0(sim_loc, "subset.len")
out_loc <- sim_loc


## set up fold change matrix ##
gtf <- readLines(gtf_loc)
names(gtf) <- seq_along(gtf)
sample <- gtf[1:(num_deg/2)]
sample2 <- gtf[(num_deg/2+1):num_deg]
idx <- as.integer(names(sample))
idx2 <- as.integer(names(sample2))

deg <- matrix(c(rep(1, 2*length(gtf))), nrow=length(gtf))
deg[idx,1] <- runif(n=length(idx), min=2, max=4)
deg[idx2,2] <- runif(n=length(idx), min=2, max=4)


## get lengths for sequencing depth calculation ##
len <- as.numeric(readLines(len_loc))
readspertx = round(depth * len / 100)
readspertx <- replace(readspertx, readspertx==0, 1)


## primary function ##
simulate_experiment(seqpath = fasta_loc, gtf = gtf_loc, reads_per_transcript=readspertx,
    num_reps=c(num_reps,num_reps), fold_changes=deg, outdir=out_loc, exononly=FALSE, 
    strand_specific=TRUE, readlen=100, add_gc_bias=sample(1:7,2,replace=TRUE), 
    error_model='illumina5')
