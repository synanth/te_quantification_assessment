#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J star_$1
#SBATCH -o /home/stexocae/li_lab/te_sim/out/align/star/$1.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/align/star/$1.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate star
python3 /home/stexocae/li_lab/te_sim/scripts/long_bench/star.py $1

EOT
