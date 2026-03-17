#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J sim_$1_$2_$3_$4
#SBATCH -o /home/stexocae/li_lab/te_sim/out/sim/$1_$2_$3_$4.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/sim/$1_$2_$3_$4.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --mem=128G

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate te_sim
Rscript /home/stexocae/li_lab/te_sim/scripts/simulate.r $1 $2 $3 $4

EOT
