import subprocess

srrs = ["SRR27494670", "SRR27494681", "SRR27494683", "SRR27494684", "SRR27494686",
        "SRR27494690", "SRR27494691", "SRR27494692", "SRR27494708", "SRR27494729",
        "SRR27494740", "SRR27494746", "SRR27494758", "SRR27494783", "SRR27494794", 
        "SRR27494805", "SRR27494813", "SRR27494824", "SRR27494858", "SRR27494859"]

base_loc = "/home/stexocae/li_lab/te_sim/scripts/aud/"
saem_ids = []

for srr in srrs:
    qc_call = "bash " + base_loc + "fastp.sh " + srr 
    qc_id = subprocess.run(qc_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
    saem_call = "bash " + base_loc + "te-saem.sh " + srr + " " + qc_id
    saem_ids += [subprocess.run(saem_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]]

matrix_call = "bash " + base_loc + "matrices.sh " + ",".join(saem_ids)
subprocess.run(matrix_call, shell=True)
