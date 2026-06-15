import subprocess

depths = ["2", "5", "10", "30", "50"]
gtfs = ["ervmap", "explorate", "lions", "squire", "telescope", "telocal", "tetools", "texp"]
slurm_loc = "/home/stexocae/li_lab/te_sim/scripts/slurm/"


for gtf in gtfs:
    for depth in depths:
        matrix_call = "bash " + slurm_loc + "matrix.sh chm13 " + gtf + " te-saem 1 " + depth
        mat_id = subprocess.run(matrix_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
        assess_call = "bash " + slurm_loc + "raw_assess.sh chm13 " + gtf + " te-saem 1 " + depth + " " + mat_id  
        subprocess.run(assess_call, shell=True)
        family_assess_call = "bash " + slurm_loc + "family_assess.sh chm13 " + gtf + " 1 " + depth + " " + mat_id
        subprocess.run(family_assess_call, shell=True)
