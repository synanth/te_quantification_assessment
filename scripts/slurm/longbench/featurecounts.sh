#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J featurecounts_$1_$2
#SBATCH -o /home/stexocae/li_lab/te_sim/out/align/fc_$1_$2.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/align/fc_$1_$2.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --dependency=afterok:$3

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate minimap
python3 /home/stexocae/li_lab/te_sim/scripts/long_bench/featurecounts.py $1 $2

EOT
