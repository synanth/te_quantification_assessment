#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J bootstrap
#SBATCH -o /home/stexocae/li_lab/te_sim/out/bootstrap.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/bootstrap.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate assess
python3 /home/stexocae/li_lab/te_sim/scripts/long_bench/downsampled.py

EOT
