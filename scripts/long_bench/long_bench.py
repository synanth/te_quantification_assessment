import subprocess

long_reads  = ["SRR30947491", "SRR30947492", "SRR30947493", "SRR30947494", 
               "SRR30947496", "SRR30947497", "SRR30947498", "SRR30947499"]
short_reads = ["SRR30947472", "SRR30947473", "SRR30947474" ,"SRR30947477", 
               "SRR30947483", "SRR30947495", "SRR30947506", "SRR30947507"]

long_to_short = {"SRR30947491" : "SRR30947472", "SRR30947492" : "SRR30947473",
                 "SRR30947493" : "SRR30947477", "SRR30947494" : "SRR30947474",
                 "SRR30947496" : "SRR30947483", "SRR30947497" : "SRR30947495",
                 "SRR30947498" : "SRR30947506", "SRR30947499" : "SRR30947507"}

methods = ["ervmap", "explorate", "lions", "squire", "te-saem", "telescope", "telocal", "tetools", "texp"]

base_loc = "/lustre/research/dawli/stexocaelum/longbench/"
slurm_loc = "/home/stexocae/li_lab/te_sim/scripts/slurm/longbench/"
fc_ids = []
quant_ids = []

## map long reads ##
for lr in long_reads:
    loc = base_loc + lr + "/" + lr
    
    map_call = "bash " + slurm_loc + "map_long.sh " + lr
    map_jobid = subprocess.run(map_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
    print(map_call)
    samtools_call = "bash " + slurm_loc + "samtools.sh " + lr + " " + map_jobid
    samtools_jobid = subprocess.run(samtools_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
    print(samtools_call)
    for method in methods:
        overlap_call = "bash " + slurm_loc + "featurecounts.sh " + lr + " " + method + " " + samtools_jobid
        fc_ids += [subprocess.run(overlap_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]]

quit()

## map short reads ##
for sr in short_reads:
    loc = base_loc + sr + "/" + sr
    bt2_call = "bash " + slurm_loc + "bowtie2.sh " + sr
    star_call = "bash " + slurm_loc + "star.sh " + sr
    
    star_id = subprocess.run(star_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
    bt2_id = subprocess.run(bt2_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
    sr_map_jobids = star_id + "," + bt2_id

    for method in methods:
        quant_call = "bash " + slurm_loc + method + ".sh " + sr + " " + sr_map_jobids
        quant_ids += [subprocess.run(quant_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]]

ids = ",".join(quant_ids + fc_ids)
