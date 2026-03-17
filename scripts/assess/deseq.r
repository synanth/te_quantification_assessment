suppressMessages(
    library("DESeq2")
)


args = commandArgs(trailingOnly=TRUE)
build <- args[[1]]
gtf_type <- args[[2]]
method <- args[[3]]
n_reps <- as.integer(args[[4]])
depth <- as.integer(args[[5]])

folder_loc <- paste0("/lustre/research/dawli/stexocaelum/TE_quantification_simulation/", build, "_", gtf_type, "_", n_reps, "_", depth, "/sim/") 
sim_counts_loc <- paste0(folder_loc, "sim_counts_matrix.csv")
quant_counts_loc <- paste0(folder_loc, method, ".csv")
sim_group_loc <- paste0(folder_loc, "sim_rep_info.txt")
sim_de_loc <- paste0(folder_loc, "sim_tx_info.txt")
de_loc <- paste0(folder_loc, method, "_de.txt")
out_loc <- paste0(folder_loc, "assess/deseq_", method, ".csv")


sim_counts <- as.matrix(read.table(file=sim_counts_loc, sep=",", row.names=1, header=TRUE))
all_names <- rownames(sim_counts)


quant_counts <- as.matrix(read.table(file=quant_counts_loc, sep=",", row.names=1, header=TRUE))
metadata <- as.matrix(read.table(file=sim_group_loc, row.names=1, header=TRUE)[,-2, drop=FALSE])
sim_de <- as.matrix(read.table(file=sim_de_loc, row.names=1, header=TRUE)[,-2, drop=FALSE])
metadata[,"group"] <- as.factor(metadata[,"group"])


## sim DE ##
dds <- DESeqDataSetFromMatrix(countData=sim_counts, colData=metadata, design=~group)
keep <- rowSums(counts(dds) >= 10) >= n_reps
dds <- dds[keep,]

suppressMessages(
    dds <- DESeq(dds, test="LRT", reduced=~1)
)
res <- results(dds)

res <- as.data.frame(res)
sim_de1 <- intersect(rownames(res)[which(res$log2FoldChange>1)], rownames(res)[which(res["padj"]<.05)])
sim_de2 <- intersect(rownames(res)[which(res$log2FoldChange<1)], rownames(res)[which(res["padj"]<.05)])
sim_nde <- setdiff(all_names, c(sim_de1, sim_de2))

if (all(quant_counts == 0)) {
    out <- paste(0, 0, 0, 0, sep=",")

    fileConnection <- file(out_loc)
    writeLines(c(out), fileConnection)
    close(fileConnection)
    quit()
}

dds <- DESeqDataSetFromMatrix(countData=quant_counts, colData=metadata, design=~group)
keep <- rowSums(counts(dds) >= 10) >= n_reps
dds <- dds[keep,]
print(dds)
if (length(rownames(counts(dds))) <= 10) {
    out <- paste(0, 0, 0, 0, sep=",")

    fileConnection <- file(out_loc)
    writeLines(c(out), fileConnection)
    close(fileConnection)
    quit()
}
suppressMessages(
    dds <- DESeq(dds, test="LRT", reduced=~1)
)
res <- results(dds)
res <- as.data.frame(res)
quant_de1 <- intersect(rownames(res)[which(res$log2FoldChange>1)], rownames(res)[which(res["padj"]<.05)])
quant_de2 <- intersect(rownames(res)[which(res$log2FoldChange<1)], rownames(res)[which(res["padj"]<.05)])
quant_nde <- setdiff(all_names, c(quant_de1, quant_de2))

n_tp <- length(intersect(quant_de1, sim_de1)) + length(intersect(quant_de2, sim_de2))
n_fp <- length(intersect(sim_nde, c(quant_de1, quant_de2)))
n_tn <- length(intersect(quant_nde, sim_nde))
n_fn <- length(intersect(c(sim_de1, sim_de2), quant_nde))

precision <- n_tp/(n_tp + n_fp)
recall <- n_tp/(n_tp+n_fn)
accuracy <- (n_tp + n_tn)/(n_tp+n_fp+n_fn+n_tn)
f1 <- 2*(precision*recall)/(precision+recall)


f1 <- replace(f1, is.na(f1), 0)
precision <- replace(precision, is.na(precision), 0)
out <- paste(precision, recall, accuracy, f1, sep=",")
out

fileConnection <- file(out_loc)
writeLines(c(out), fileConnection)
close(fileConnection)
