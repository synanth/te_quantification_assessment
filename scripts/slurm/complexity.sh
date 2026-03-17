#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J complexity_$1
#SBATCH -o /home/stexocae/li_lab/te_sim/out/assess/complexity_$1.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/sim/complexity_$1.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --dependency=afterok:$1
#SBATCH --exclude=cpu-24-[1-60]


. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate te_sim
python3 /home/stexocae/li_lab/te_sim/scripts/assess/complexity.py $1

EOT
