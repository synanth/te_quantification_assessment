#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J te-saem_$1
#SBATCH -o /home/stexocae/li_lab/te_sim/out/quant/te-saem/$1.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/quant/te-saem/$1.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem=70GB
##SBATCH --dependency=afterok:$2


. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate saem
python3 /home/stexocae/li_lab/saem/te-saem.py -1 /lustre/research/dawli/stexocaelum/me_cfs2/$1/$1_pqc_1.fastq -2 /lustre/research/dawli/stexocaelum/me_cfs2/$1/$1_pqc_2.fastq -o /lustre/research/dawli/stexocaelum/me_cfs2/$1/te_counts.csv

EOT
