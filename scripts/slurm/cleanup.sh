#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J cleanup_$1_$2_$3_$4
#SBATCH -o /home/stexocae/li_lab/te_sim/out/sim/clean_$1_$2_$3_$4.e%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/sim/clean_$1_$2_$3_$4.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --dependency=afterok:$5
#SBATCH --exclude=cpu-24-[1-60]

python3 /home/stexocae/li_lab/te_sim/scripts/helpers/cleanup.py $1 $2 $3 $4

EOT
