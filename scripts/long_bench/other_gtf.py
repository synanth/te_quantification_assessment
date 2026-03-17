import subprocess

short_reads = ["SRR30947472", "SRR30947473", "SRR30947474" ,"SRR30947477", 
               "SRR30947483", "SRR30947495", "SRR30947506", "SRR30947507"]
gtfs = ["ervmap", "telescope"]

base_slurm_loc = "/home/stexocae/li_lab/te_sim/scripts/slurm/longbench/other_gtf_te-saem.sh"

for gtf in gtfs:
    for sr in short_reads:
        slurm_call = "bash " + base_slurm_loc + " " + gtf + " " + sr
        print(slurm_call)
        subprocess.run(slurm_call, shell=True)
