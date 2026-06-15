#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J aud2_matrix
#SBATCH -o /home/stexocae/li_lab/te_sim/out/quant/te-saem/aud2_matrix.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/quant/te-saem/aud2_matrix.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --dependency=afterok:$1


. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate saem
python3 /home/stexocae/li_lab/te_sim/scripts/aud2/matrices.py

EOT
