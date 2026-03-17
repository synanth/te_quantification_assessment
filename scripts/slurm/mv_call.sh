#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J mv_$1_$2_$3_$4
#SBATCH -o /home/stexocae/li_lab/te_sim/out/sim/mv_$1_$2_$3_$4.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/sim/mv_$1_$2_$3_$4.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --dependency=afterok:$5

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate te_sim
echo 'move'
python3 ~/li_lab/te_sim/scripts/helpers/mv_call.py $1 $2 $3 $4
echo 'convert rda'
Rscript ~/li_lab/te_sim/scripts/quant/helpers/translate/convert_rda.r $1 $2 $3 $4
#echo 'convert simcounts to tecount'
#python3 ~/li_lab/te_sim/scripts/quant/helpers/translate/sim_tecount.py $1 $2 $3 $4

EOT
