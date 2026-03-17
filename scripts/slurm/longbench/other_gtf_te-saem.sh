#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J $1_$2
#SBATCH -o /home/stexocae/li_lab/te_sim/out/quant/te-saem/$1_$2.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/quant/te-saem/$1_$2.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate saem
mkdir /lustre/research/dawli/stexocaelum/longbench/$2/te-saem/$1/
cp /lustre/research/dawli/stexocaelum/longbench/$2/te-saem/star.sam /lustre/research/dawli/stexocaelum/longbench/$2/te-saem/$1/


python3 /home/stexocae/li_lab/saem/scripts/parse_alignment.py -t 16 -g /lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/$1.gtf -s /lustre/research/dawli/stexocaelum/longbench/$2/te-saem/$1/star.sam

python3 /home/stexocae/li_lab/saem/scripts/saem.py -d /lustre/research/dawli/stexocaelum/longbench/$2/te-saem/$1/ -g /lustre/work/stexocae/li_lab/refs/te_annotations/simulation/chm13/$1.gtf -o /lustre/research/dawli/stexocaelum/longbench/$2/te-saem/$1/counts.out

EOT
