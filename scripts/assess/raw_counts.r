#library(SMFilter)
#library(FactoMineR)
#library(mvcor)
#library(rrcov3way)
#library(philentropy)
#library(fastmatch)

args = commandArgs(trailingOnly=TRUE)
build <- args[[1]]
gtf_type <- args[[2]]
method <- args[[3]]
n_reps <- as.integer(args[[4]])
depth <- as.integer(args[[5]])

folder_loc <- paste0("/lustre/research/dawli/stexocaelum/TE_quantification_simulation/", build,  "_", gtf_type, "_", n_reps, "_", depth, "/sim/") 
sim_counts_loc <- paste0(folder_loc, "sim_counts_matrix.csv")
quant_counts_loc <- paste0(folder_loc, method, ".csv")
out_loc <- paste0(folder_loc , "assess/raw_", method, ".csv")


header <- paste("jsd", "euclidean", "mard", "congruence", "sensitivity", "precision", sep=",")
mard <- function(true, pred) {
    true <- head(true, -1)
    pred_tail <- tail(pred,1)
    pred <- head(pred, -1)
    mardi <- (sum(abs(true-pred)/true) + sum(pred_tail))*(1/(length(true)+1))
    return(mardi)
}

confusion <- function(true, pred) {
    tp = 0
    fp = 0
    fn = 0
    diff <- unlist(as.list(true - pred))
    true <- unlist(as.list(true))
    pred <- unlist(as.list(pred))
    for (x in 1:length(diff)) {
        if (diff[[x]] >= 1) {
            tp = tp + pred[[x]]
            fn = fn + diff[[x]]
        }
        else if (diff[[x]] <= 0) {
            fp = fp + (-1 * diff[[x]])
            tp = tp + true[[x]]
        }
    }
    sensitivity <- tp/(tp+fn)
    precision <- tp/(tp+fp)
    print(sensitivity)
    print(precision)
    return(list(sensitivity, precision))
}


#load(sim_counts_loc)
counts_matrix = read.csv(sim_counts_loc,row.names=1,stringsAsFactors=F)
quant_counts = read.csv(quant_counts_loc,row.names=1,stringsAsFactors=F)
quant_counts <- quant_counts[order(rownames(quant_counts)),]

if( all(quant_counts == 0)){
    print("All counts are zero, methinks an error is afoot.")
    out = "0,0,0,0,0,0"
    fileConnection <- file(out_loc)
    writeLines(c(header, out), fileConnection)
    close(fileConnection)
    quit()
}

head(counts_matrix)
head(quant_counts)
dim(counts_matrix)
dim(quant_counts)

spearman <- cor(counts_matrix$sample_01, quant_counts$sample_01, method="spearman")

ret <-confusion(counts_matrix, quant_counts)
sensitivity <- ret[[1]]
precision <- ret [[2]]

f1 <- 2 * ((precision * sensitivity)/(precision + sensitivity))

header <- paste("spearman", "sensitivity", "precision", "f1", sep=",")
out <- paste(spearman, sensitivity, precision, f1, sep=",")

print(out)
fileConnection <- file(out_loc)
writeLines(c(header, out), fileConnection)
close(fileConnection)
