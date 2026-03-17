#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J family_$1_$2_$3_$4
#SBATCH -o /home/stexocae/li_lab/te_sim/out/assess/family_$1_$2_$3_$4.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/assess/family_$1_$2_$3_$4.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --dependency=afterok:$5

python3 /home/stexocae/li_lab/te_sim/scripts/assess/family.py $1 $2 $3 $4

EOT
