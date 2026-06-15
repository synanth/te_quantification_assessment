#############################################
#                                           #
#   deseq2                                  #
#       to-do:                              #
#           -- aggregated counts            #
#           -- pc regression                #
#           -- plsda                        #
#           -- fancy box plots              #
#                                           #
#############################################

suppressPackageStartupMessages({
    library("DESeq2")
    library("magrittr")
    library("tibble")
    library("pheatmap")
    library("EnhancedVolcano")
})

base_loc <- "/lustre/research/dawli/stexocaelum/me_cfs2/"
deg_loc <- paste0(base_loc, "deg/")
counts_loc <- paste0(base_loc, "counts.csv")
metadata_loc <- paste0(base_loc, "metadata.csv")

count_matrix <- as.matrix(read.csv(counts_loc, row.names=1))
keep <- rowSums(count_matrix >= 5) >= 3
count_matrix <- count_matrix[keep,]
coldata <- read.csv(metadata_loc, row.names=1)
idx <- sort(intersect(colnames(count_matrix), rownames(coldata)))
coldata <- coldata[idx,, drop=FALSE]
count_matrix <- count_matrix[,idx]
print("test")
## helper functions
get_upregulated <- function(df){
    key <- intersect(rownames(df)[which(df$log2FoldChange>=1)], rownames(df)[which(df["padj"]<=0.05)])
    results <- key
    return(results)
}            
get_downregulated <- function(df){
   key <- intersect(rownames(df)[which(df$log2FoldChange<=-1)], rownames(df)[which(df["padj"]<=0.05)])
    results <- key
    return(results)
}
coldata$condition <- factor(coldata[["condition"]])
coldata$condition <- relevel(coldata$condition, ref="control")


print("test2")
## create dds object
suppressMessages({
    dds <- DESeqDataSetFromMatrix(countData = count_matrix, colData = coldata, design = ~condition)
})

deg_loc <- "/home/stexocae/data_xfer/me2_degs.csv"
vsd_loc <- "/home/stexocae/data_xfer/me2_vsd.csv"

dds <- DESeq(dds)
res <- results(dds, alpha=0.05, lfcThreshold=.5) #independentFiltering=TRUE, cooksCutoff=FALSE)
summary(res)
res_df <- as.data.frame(res)
write.csv(res_df, deg_loc, quote=FALSE)





vsd <- vst(dds, blind=FALSE)
vsd <- assay(vsd)
head(vsd)
vsd_df <- as.data.frame(vsd)
write.csv(vsd_df, vsd_loc, quote=FALSE)


print(get_upregulated(res_df))
print(get_downregulated(res_df))
