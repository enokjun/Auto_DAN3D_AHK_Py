"""
Creator: Enok Cheon
Date: 2019-06-04
Programming: Python, AutoHotKey(AHK)
License: MIT License
Purpose: automate DAN3D simulation and determine the barrier location

## generate dn3 files for DAN3D
"""

# json pretty print of dictionaries
def print_json_dict(dictionary, order=False, indenting=4):
	import json
	print(json.dumps(dictionary, indent=indenting, sort_keys=order))
	return None

def generateDN3(inputFileName):

	## sort the input data
	inputFileNameList = inputFileName.split('.')
	if len(inputFileNameList) == 2: # only one period occurs
		inputFileNameOnly = inputFileNameList[0]
	else:
		inputFileNameOnly = ''
		for loopName in range(len(inputFileNameList)-1):
			inputFileNameOnly += inputFileNameList[loopName]
			if loopName < len(inputFileNameList)-2:
				inputFileNameOnly += inputFileNameList[loopName]

	# step 1 - read the file line by line
	inputFileAll_list = []
	with open(inputFileName,'r') as f:
		ff=f.read().split('\n')
		#ff=f.read().replace('\n','\t').split('\t')
		inputFileAll_list.append(ff)
	inputFileAll_list = inputFileAll_list[0]
	#print(inputFileAll_list)

	# step 2 - sort data between the project title (even integer) and data (odd integer)
	inputFileAll_list2 = []
	for r in inputFileAll_list:
		# find the delimiter
		if ',' in r:
			delim = ','
		elif '\t' in r:
			delim = '\t'

		# separate text info into lists
		try:
			rr = r.split(delim)
		except:
			print('check the input file delimiter')
			assert(1!=1)

		# eliminiate blank elements
		inputFileAll_list2.append([x for x in rr[1:] if x != ''])

	#print(inputFileAll_list2)
	
	## step 3 - create dictionary of all the input files
	project_num = len(inputFileAll_list2[0])	# total number of projects

	# list of key informations 
	key_list_part1 = ['global_file_location','dn3_name','project','data','input','material_number','particle_number','erosion_rate','smooth_length','velocity_smoothing','stiffness','slide_margin_cutoff','max_simulation_time','simulation_time','path','source']
	key_list_output = ['parts','thick','erode','maxthick','maxvel','velX','velY','velZ','depth','surf','vel','dis','maxdis']
	key_list_material = ['name', 'unit_weight', 'type', 'shear', 'phi', 'friction_coeff', 'Ru', 'viscosity', 'turbulance_coeff', 'power_law', 'int_phi', 'max_erosion_depth']
	'''
	material_factor_dict = {
		'frictional': [1, ['phi', 'Ru']],
		'plastic': [2, ['shear']],
		'newtonian': [3, ['viscosity']],
		'bingham': [5, ['shear', 'viscosity']],
		'voellmy': [8, ['friction coeff', 'turbulance coeff']]
	}
	'''
	material_factor_dict = {
		'frictional': [1, [4,5], [4,6]],
		'plastic': [2, [3], [3]],
		'newtonian': [3, [6], [7]],
		'bingham': [5, [3,6], [3,7]],
		'voellmy': [8, [7,8], [5,8]]
	}

	## create dictionary of all the input files
	# keys = number of project , values = project dictionary (keys = information, value = data)
	project_dic = {}
	erosionID = 0
	materialID = 0
	for ID in range(project_num):
		rowID = 0
		tempDic = {}

		# up to source map
		for nn in range(len(key_list_part1)):
			tempDic[key_list_part1[nn]] = inputFileAll_list2[nn][ID]
			rowID += 1

		# erosion map
		if int(tempDic['material_number']) == 1:
			tempDic['erosion'] = None
		else:
			tempDic['erosion'] = inputFileAll_list2[rowID][erosionID]
			erosionID += 1
		rowID += 1

		# output time interval
		tempDic['output_time_interval'] = inputFileAll_list2[rowID][ID]
		rowID += 1

		# output options
		output_list = []
		for oo in range(rowID, rowID+len(key_list_output)):
			output_list.append(inputFileAll_list2[oo][ID])
		tempDic['output_list'] = output_list
		rowID += len(key_list_output)

		# material names
		tempDic['material'] = []

		for loopMat in range(int(tempDic['material_number'])):
			
			tempMat_list = ['0']*len(key_list_material)

			# 'name', 'unit weight', 'int phi', 'max erosion depth' 
			for matIDX in [rowID, rowID+2, rowID+len(key_list_material)-2, rowID+len(key_list_material)-1]:
				tempMat_list[matIDX-rowID] = inputFileAll_list2[matIDX][materialID]

			tempMat_list[1] = tempMat_list[2]	# switch position of unit weight into 2nd position 

			# 'type' ID number
			tempMat_list[2] = str(material_factor_dict[inputFileAll_list2[rowID+1][materialID]][0])

			# soil parameters
			soil_para_list_in = material_factor_dict[inputFileAll_list2[rowID+1][materialID]][1]
			soil_para_list_out = material_factor_dict[inputFileAll_list2[rowID+1][materialID]][2]
			for IDX_in,IDX_out in zip(soil_para_list_in, soil_para_list_out):
				tempMat_list[IDX_out] = inputFileAll_list2[rowID+IDX_in][materialID]

			tempDic['material'].append(tempMat_list)
			materialID += 1 

		project_dic[ID] = tempDic
			
	## generate a text file of all the file names + file locations
	import xlsxwriter as xw

	workbook = xw.Workbook(project_dic[0]['global_file_location']+'\\'+'03_dn3_file_names_'+inputFileNameOnly+'.xlsx')	# create and save the xlsx file
	worksheet = workbook.add_worksheet()	

	for ID in range(project_num):
		#project_dic[ID]['global_file_location']+'\\'+project_dic[ID]['dn3_name']+'.dn3'		# dn3 file location
		worksheet.write('A'+str(ID+1), project_dic[0]['global_file_location']+'\\'+project_dic[ID]['dn3_name']+'.dn3')
		worksheet.write('B'+str(ID+1), project_dic[ID]['max_simulation_time'])

	workbook.close()	# finish creating the xlsx file

	## generate csv with file names
	dn3_file_name_list = []
	for ID in range(project_num):
		dn3_file_name_list.append(project_dic[ID]['dn3_name'])

	csvFileName = project_dic[ID]['global_file_location']+'\\'+'03_dn3_file_names_'+inputFileNameOnly+'_name_list.csv'

	import csv
	with open(csvFileName, 'w', newline='') as csvfile:
	    rowwriter = csv.writer(csvfile, delimiter=',')
	    for i in dn3_file_name_list:
		    rowwriter.writerow([i])
	csvfile.close()

	## generate dn3 files
	for ID in range(project_num):

		dn3File = project_dic[ID]['global_file_location']+'\\'+project_dic[ID]['dn3_name']+'.dn3'+'\n'		# dn3 file location

		# from 'project' to 'simulation time'
		for keys in key_list_part1[2:-2]:
			if keys == 'slide_margin_cutoff':
				continue
			else:
				dn3File += project_dic[ID][keys]+'\n'

		dn3File += project_dic[ID]['output_time_interval']+'\n'		
		dn3File += '1'+'\n'		# output during simulation or not
		dn3File += '\"'+project_dic[ID]['global_file_location']+'\\'+project_dic[ID]['project']+'\"'+'\n'		# output folder location
		
		dn3File += project_dic[ID]['slide_margin_cutoff']+'\n'
		dn3File += '1'+'\n'		# number of timesteps to be run between each screen update 

		# backgroun image - don't include for now
		dn3File += '\"\"\n'+'0\n'+'0\n'+'1\n'+'1\n'+'0\n'+'0\n'+'1\n'+'1\n'

		dn3File += '#TRUE#'+'\n'  # set legend max. and min. automatically
		dn3File += '0,50'+'\n'	#legend Minimum, Legend Maximum (default: 0,50) [Options - Display]
		dn3File += '1'+'\n'		# Grid Point draw size (default=1)

		# export options
		for option in project_dic[ID]['output_list']:
			dn3File += option+'\n'

		dn3File += project_dic[ID]['global_file_location']+'\\'+project_dic[ID]['path']+'.grd'+'\n'		# path locations
		dn3File += project_dic[ID]['global_file_location']+'\\'+project_dic[ID]['source']+'.grd'+'\n'	# source locations

		if int(project_dic[ID]['material_number']) > 1:
			dn3File += project_dic[ID]['global_file_location']+'\\'+project_dic[ID]['erosion']+'.grd'+'\n'	# erosion locations

		# material information
		material_list = project_dic[ID]['material']
		for loopM in range(int(project_dic[ID]['material_number'])):
			for loopMpara in range(len(material_list[0])):
				dn3File += material_list[loopM][loopMpara]+'\n'	

		# create the export directory folder
		import os
		os.mkdir(project_dic[ID]['global_file_location']+'\\'+project_dic[ID]['project'])

		# export file
		with open(project_dic[ID]['global_file_location']+'\\'+project_dic[ID]['dn3_name']+'.dn3', 'w') as f:
			f.write(dn3File)
	
if __name__ == "__main__":
	generateDN3('01_dan3d_input_example.csv')

