import subprocess

srrs= ["SRR8961823", "SRR8961824", "SRR8961825", "SRR8961826", "SRR8961827",
       "SRR8961828", "SRR8961829", "SRR8961830", "SRR8961831", "SRR8961832",
       "SRR8961833", "SRR8961834", "SRR8961835", "SRR8961836", "SRR8961837",
       "SRR8961838", "SRR8961839", "SRR8961840", "SRR8961841", "SRR8961842"]

base_loc = "/home/stexocae/li_lab/te_sim/scripts/me_cfs/"
saem_ids = []

for srr in srrs:
    qc_call = "bash " + base_loc + "fastp.sh " + srr 
    qc_id = subprocess.run(qc_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
    saem_call = "bash " + base_loc + "te-saem.sh " + srr + " " + qc_id
    saem_ids += [subprocess.run(saem_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]]

matrix_call = "bash " + base_loc + "matrices.sh " + ",".join(saem_ids)
subprocess.run(matrix_call, shell=True)
