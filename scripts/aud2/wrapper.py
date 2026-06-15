import subprocess

srrs = ["SRR27494667", "SRR27494668", "SRR27494669", "SRR27494671", "SRR27494672",
        "SRR27494673", "SRR27494674", "SRR27494676", "SRR27494719", "SRR27494720",
        "SRR27494666", "SRR27494675", "SRR27494677", "SRR27494678", "SRR27494679",
        "SRR27494680", "SRR27494682", "SRR27494685", "SRR27494687", "SRR27494688"]

base_loc = "/home/stexocae/li_lab/te_sim/scripts/aud2/"
saem_ids = []

for srr in srrs:
    qc_call = "bash " + base_loc + "fastp.sh " + srr 
    qc_id = subprocess.run(qc_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]
    saem_call = "bash " + base_loc + "te-saem.sh " + srr + " " + qc_id
    saem_ids += [subprocess.run(saem_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()[-1]]

matrix_call = "bash " + base_loc + "matrices.sh " + ",".join(saem_ids)
subprocess.run(matrix_call, shell=True)
