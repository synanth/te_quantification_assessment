#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J viz_$1_$2_$3_$4
#SBATCH -o /home/stexocae/li_lab/te_sim/out/viz/$1_$2_$3_$4.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/viz/$1_$2_$3_$4.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem=32G
#SBATCH --dependency=afterok:$5
#SBATCH --exclude=cpu-24-[1-60]

source activate viz
python3 /home/stexocae/li_lab/te_sim/scripts/viz/raw.py $1 $2 $3 $4
python3 /home/stexocae/li_lab/te_sim/scripts/viz/family_raw.py $1 $2 $3 $4
python3 /home/stexocae/li_lab/te_sim/scripts/viz/deseq.py $1 $2 $3 $4
python3 /home/stexocae/li_lab/te_sim/scripts/viz/complexity.py $1 $2 $3 $4

EOT
