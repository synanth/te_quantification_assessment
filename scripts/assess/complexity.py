import sys
import subprocess

job_id = sys.argv[1] 

sacct_call = "sacct --format=\"JobName%50,AllocCPUS%10\" -j " + job_id
sacct_output = subprocess.run(sacct_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split()
name = sacct_output[4]
alloc_cpus = sacct_output[5]

print(name)

folder = "_".join(name.split("_")[3:])
split = name.split("_")
folder = "_".join([split[1], split[2], split[5], split[6]])
method = name.split("_")[0]
sample = "_".join(name.split("_")[1:3])

seff_call = "seff " + job_id
complexity_output = subprocess.run(seff_call, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip().split("\n")
time = complexity_output[8].split()[-1].split(":")
if "-" in time[0]:
    time[0] = str(int(time[0].split("-")[0])*24 + int(time[0].split("-")[1]))

mins = int(time[0]) * 60 + int(time[1]) + round(int(time[2])/60)
if complexity_output[9].split()[-1] == "MB":
    print("mb")
    mem = str(float(complexity_output[9].split()[-2]) / 1024)
else:
    print("gb")
    mem = complexity_output[9].split()[-2]

cpu = complexity_output[6].split()[-1].split(":")
if "-" in cpu[0]:
    cpu[0] = str(int(cpu[0].split("-")[0])*24 + int(cpu[0].split("-")[1]))
cpu = int(cpu[0])*60 + int(cpu[1]) + round(int(cpu[2])/60) 


out = method + "," + sample + "," + str(mins) + "," + mem + "," + alloc_cpus + "," + str(cpu)
print(out)

out_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/" + folder + "/sim/assess/complexity_" + method + ".csv"

with open(out_loc, "a") as f:
    f.write(out + "\n")
