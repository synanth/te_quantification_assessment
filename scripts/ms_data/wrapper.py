import subprocess

srrs = ["SRR10248405", "SRR10248406", "SRR10248407", "SRR10248408", "SRR10248439",
        "SRR10248404", "SRR10248411", "SRR10248419", "SRR10248421", "SRR10248427"]

base_loc = "/home/stexocae/li_lab/te_sim/scripts/ms_data/"
saem_ids = []

for srr in srrs:
    qc_call = "bash " + base_loc + "fastp.sh " + srr 
    qc_id = subprocess.run(qc_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
    saem_call = "bash " + base_loc + "te-saem.sh " + srr + " " + qc_id
    saem_ids += [subprocess.run(saem_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]]

matrix_call = "bash " + base_loc + "matrices.sh " + ",".join(saem_ids)
subprocess.run(matrix_call, shell=True)
