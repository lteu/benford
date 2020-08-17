'''
This script runs solvers on MZNC instances

run with python3 main.py
'''

import glob
import os
import time
import sys
from shutil import copyfile
import socket
from subprocess import Popen

def runCases(scenario):
	# compile_cmd = "../netprog/minizinc-2.1.2/bin/mzn2fzn -I "+mznlib+" mznc2019_probs/accap/accap.mzn mznc2019_probs/accap/accap_instance3.dzn -o xxx.fzn"
	# aCase = scenarios[8]

	aCase = scenario

	mzn2fzn = "../netprog/minizinc-2.1.2/bin/mzn2fzn"
	solver = "bin/fzn_chuffed"
	mznlib = "mznlib/chuffed"
	ist_str = ""
	outdir  = "output"

	solvername = solver.split("/")[1]
	compile_cmds = []
	if len(aCase[1]) == 0:
		for istModel in aCase[0]:
			ist_str = istModel
			compile_cmd = mzn2fzn+ " -I "+mznlib+" "+ist_str+" -o xxx.fzn"
			compile_cmds.append([compile_cmd,ist_str])
	else:
		istModel = aCase[0][0]
		for ist in aCase[1]:
			ist_str = istModel + " "+  ist
			compile_cmd = mzn2fzn+ " -I "+mznlib+" "+ist_str+" -o xxx.fzn"
			compile_cmds.append([compile_cmd,ist])

	exe_cmd = solver + " xxx.fzn"



	counter = 0
	for case in compile_cmds:
		name = case[1]
		try:
			cmd = "timeout 300 "+ case[0]

			print("compiling: "+cmd)

			proc = Popen(cmd.split())
			proc.communicate()
		except:
			print("Compilation FAILED:"+cmd)
			continue


		try:
			exe_cmd_case ="timeout 1200 "+ exe_cmd
			print("running: "+exe_cmd_case)
			rlt = os.popen(exe_cmd_case).read()
		except:
			print("Runtime FAILED:"+exe_cmd_case)
			# continue

		filename = name.replace("/","-")
		text_file = open(outdir+"/"+solvername+"-"+filename+".txt", "w+")
		text_file.write(name+"\n"+rlt)
		text_file.close()

		counter+=1


def getModelAndInstances(path):
	modefile = []
	instances = []
	for subdir in os.listdir(path):
		item = path+"/"+subdir
		# print(item)
		if not os.path.isfile(item):
			continue

		suffix = item[-3:]

		if suffix == 'dzn':
			instances.append(item)
		elif suffix == 'mzn':
			# if modefile != "":
			# 	sys.exit("check"+path+"; more mzn files present !!!")
			modefile.append(item)

		# print(item,suffix)

	return modefile, instances

# ==============================
# 			MAIN
# ==============================


def main(args):
	case_folder = "mznc2019_probs"
	# run(case_folder)

	scenarios = []
	for subdir in os.listdir(case_folder):
		path = case_folder+"/"+subdir
		if not os.path.isdir(path):
			continue
		modefile, instances = getModelAndInstances(path)
		# print(modefile,instances)

		scenarios.append([modefile,instances])
		# sys.exit()
    # print("\nIt is a directory")  
		# print(path)

	for scenario in scenarios:
		runCases(scenario)


if __name__ == '__main__':
	main(sys.argv[1:])










