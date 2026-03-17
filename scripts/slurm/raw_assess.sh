#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J raw_$1_$2_$3_$4_$5
#SBATCH -o /home/stexocae/li_lab/te_sim/out/assess/raw_$1_$2_$3_$4_$5.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/assess/raw_$1_$2_$3_$4_$5.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem=32G
#SBATCH --dependency=afterok:$6
#SBATCH --exclude=cpu-24-[1-60]

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate assess
Rscript /home/stexocae/li_lab/te_sim/scripts/assess/raw_counts.r $1 $2 $3 $4 $5

EOT
