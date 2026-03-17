## This program converts .rda to .csv ##

## parameters ##
args = commandArgs(trailingOnly=TRUE)
build <- args[[1]]
gtf_type <- args[[2]]
n_reps <- as.integer(args[[3]])
depth <- as.integer(args[[4]])


## file management ##
folder_loc <- paste0("/lustre/research/dawli/stexocaelum/TE_quantification_simulation/", build, "_", gtf_type, "_", n_reps, "_", depth, "/sim/") 
sim_counts_loc <- paste0(folder_loc, "sim_counts_matrix.rda")
out_loc <- paste0(folder_loc , "sim_counts_matrix.csv")


## conversion ##
load(sim_counts_loc)
counts_matrix <- rbind(counts_matrix,0)

rownames(counts_matrix)[rownames(counts_matrix) == ""] <- "unrepresented"
write.csv(counts_matrix, file=out_loc, quote=FALSE)
