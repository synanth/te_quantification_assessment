#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J supp_telescope_$1_$2
#SBATCH -o /home/stexocae/li_lab/te_sim/out/quant/telescope/$1_$2.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/quant/telescope/$1_$2.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate telescope
python3 /home/stexocae/li_lab/te_sim/scripts/quant/supp_telescope.py $1 $2 

EOT
