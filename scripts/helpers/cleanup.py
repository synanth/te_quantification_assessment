import sys
import subprocess

build = sys.argv[1]
gtf = sys.argv[2]
n_reps = sys.argv[3]
depth = sys.argv[4]

base_loc = "/lustre/research/dawli/stexocaelum/TE_quantification_simulation/"
experiment_loc = base_loc + build + "_" + gtf + "_" + n_reps + "_" + depth + "/sim/assess/*"
out_loc = base_loc + "assess/" + build + "/" + gtf + "_" + n_reps + "_" + depth + "/"

mkdir_call = "mkdir " + out_loc
cp_call = "cp " + experiment_loc + " " + out_loc

subprocess.run(mkdir_call, shell=True)
subprocess.run(cp_call, shell=True)
