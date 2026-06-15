#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J ms_matrix
#SBATCH -o /home/stexocae/li_lab/te_sim/out/quant/te-saem/me_matrix.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/quant/te-saem/me_matrix.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --dependency=afterok:$1


. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate saem
python3 /home/stexocae/li_lab/te_sim/scripts/me_cfs/matrices.py

EOT
