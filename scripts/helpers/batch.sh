#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J batch
#SBATCH -o /home/stexocae/li_lab/te_sim/out/batch.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/batch.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem=30GB

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate batch
python3 /home/stexocae/li_lab/te_sim/scripts/helpers/batch.py

EOT
