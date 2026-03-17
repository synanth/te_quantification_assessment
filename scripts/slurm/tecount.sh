#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J tecount_$1_$2_$3_$4_$5
#SBATCH -o /home/stexocae/li_lab/te_sim/out/quant/tecount/$1_$2_$3_$4_$5.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/quant/tecount/$1_$2_$3_$4_$5.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --mem=48G
#SBATCH --dependency=afterok:$6
#SBATCH --exclude=cpu-24-[1-60]

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate tetranscripts
python3 /home/stexocae/li_lab/te_sim/scripts/quant/tecount.py $1 $2 $3 $4 $5

EOT
