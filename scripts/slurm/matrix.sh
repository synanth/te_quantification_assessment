#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J matrix_$1_$2_$3_$4_$5
#SBATCH -o /home/stexocae/li_lab/te_sim/out/sim/matrix_$1_$2_$3_$4_$5.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/sim/matrix_$1_$2_$3_$4_$5.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --dependency=afterok:$6

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate te_sim
python3 /home/stexocae/li_lab/te_sim/scripts/helpers/make_count_matrix.py $1 $2 $3 $4 $5

EOT
