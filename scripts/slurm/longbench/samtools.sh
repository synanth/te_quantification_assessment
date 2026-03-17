#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J filter_$1
#SBATCH -o /home/stexocae/li_lab/te_sim/out/align/filter_$1.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/align/filter_$1.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --dependency=afterok:$2

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate minimap
python3 /home/stexocae/li_lab/te_sim/scripts/long_bench/samtools.py $1

EOT
