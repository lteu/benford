'''
This script makes Benford statistics

run with python3 stats.py
'''


import os
import sys
import matplotlib.pyplot as plt 

def extractArray(filecontent):
	rlt = []
	blocks = filecontent.split('\n')
	for b in blocks:
		if 'array2d' in b or 'array1d' in b or 'array3d' in b or 'array4d' in b:
			arr = b.split("[")[1].split("]")[0].split(',')
			arr = [i.strip() for i in arr]
			rlt.append(arr)

	return rlt

def extractVar(filecontent):
	blocks = filecontent.split('\n')
	rlt = []
	for b in blocks:
		if 'array2d' in b or 'array1d' in b or 'array3d' in b or 'array4d' in b:
			continue
		if "=" not in b:
			continue
		val = b.split("=")[1].replace(";","").strip()
		rlt.append(val)

	return rlt

def extractObj(filecontent):
	blocks = filecontent.split('\n')
	for b in blocks:
		if 'objective' in b:
			obj = b.split("objective =")[1].replace(";","").strip()
			return obj

	return ""


def makeAnalysis(dataset):
	obj_stats = {str(i):0 for i in range(10)}
	arr_stats = {str(i):0 for i in range(10)}

	for item in dataset:
		filename = item[0]
		filecontent = item[1]

		if filecontent == "":
			continue

		# debug
		# print(filecontent)
		# print(extractArray(filecontent))
		# print(extractVar(filecontent))

		arrInfo = extractArray(filecontent)
		for anArr in arrInfo:
			if len(anArr) != 0:
				for elm in anArr:
					if elm[0] in arr_stats:
						arr_stats[elm[0]] += 1


		tmpObj = extractObj(filecontent)
		if tmpObj != "":
			obj_stats[tmpObj[0]] += 1


	# plot OBJ
	labels = [str(i) for i in range(10)]
	vals = [obj_stats[l] for l in labels]
	plt.bar(labels, vals, tick_label = labels, width = 0.8) 
	plt.xlabel('Initial letter') 
	plt.ylabel('Frequency') 
	plt.title('Benford stats for MZNC 2017-2019 COPs - obj values') 
	plt.show() 

	# plot array
	# labels = [str(i) for i in range(10)]
	# vals = [arr_stats[l] for l in labels]
	# plt.bar(labels, vals, tick_label = labels, width = 0.8) 
	# plt.xlabel('Initial letter') 
	# plt.ylabel('Frequency') 
	# plt.title('Benford stats for MZNC 2017-2019 - Arrays') 
	# plt.show() 

	# print(obj_stats)
	# print(arr_stats)


def loadFile(path):

	with open(path, 'r') as f:
	# 	print(path)
		content = f.read()
		if '----------' in content:
			lastPart = content.split("----------")[-2]
			return lastPart

	return ""


def main(args):
	case_folder = "output"
	dataset = []
	for subdir in os.listdir(case_folder):
		path = case_folder+"/"+subdir
		if not os.path.isfile(path):
			continue

		# check validity
		if not 'fzn_chuffed' in path:
			continue

		result = loadFile(path)
		# print(result)
		dataset.append([path,result])

	makeAnalysis(dataset)


if __name__ == '__main__':
	main(sys.argv[1:])










