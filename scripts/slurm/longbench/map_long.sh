#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J long_read_align
#SBATCH -o /home/stexocae/li_lab/te_sim/out/align/longreads_$1.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/align/longreads_$1.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate minimap
python3 /home/stexocae/li_lab/te_sim/scripts/long_bench/map_long.py $1

EOT
