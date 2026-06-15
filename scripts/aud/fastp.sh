#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH -J fastp_$1
#SBATCH -o /home/stexocae/li_lab/te_sim/out/quant/te-saem/$1_fastp.o%j
#SBATCH -e /home/stexocae/li_lab/te_sim/out/quant/te-saem/$1_fastp.e%j
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36

. "/home/stexocae/miniconda3/etc/profile.d/conda.sh"
conda activate qc
fastp -i /lustre/research/dawli/stexocaelum/nac_aud/$1/$1_1.fastq -I /lustre/research/dawli/stexocaelum/nac_aud/$1/$1_2.fastq -o /lustre/research/dawli/stexocaelum/nac_aud/$1/$1_pqc_1.fastq -O /lustre/research/dawli/stexocaelum/nac_aud/$1/$1_pqc_2.fastq -q 20 --cut_front --cut_front_window_size 1 --cut_tail -l 20 -j /dev/null -h /dev/null


EOT
