#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J bowtie2_$1
#SBATCH -o /home/stexocae/li_lab/te_sim/out/align/bowtie2/$1.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/align/bowtie2/$1.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36


. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate bowtie
python3 /home/stexocae/li_lab/te_sim/scripts/long_bench/bowtie2.py $1

EOT
