import subprocess

srrs = ["SRR23867362", "SRR23867397", "SRR23867398", "SRR23867399", "SRR23867400",
        "SRR23867426", "SRR23867427", "SRR23867431", "SRR23867432", "SRR23867425",
        "SRR23867479", "SRR23867480", "SRR23867484", "SRR23867485", "SRR23867486",
        "SRR23867302", "SRR23867303", "SRR23867304", "SRR23867315", "SRR23867389"]

base_loc = "/home/stexocae/li_lab/te_sim/scripts/me_cfs2/"
saem_ids = []

for srr in srrs:
    qc_call = "bash " + base_loc + "fastp.sh " + srr 
    qc_id = subprocess.run(qc_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
    saem_call = "bash " + base_loc + "te-saem.sh " + srr + " " + qc_id
    saem_ids += [subprocess.run(saem_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]]

matrix_call = "bash " + base_loc + "matrices.sh " + ",".join(saem_ids)
subprocess.run(matrix_call, shell=True)
