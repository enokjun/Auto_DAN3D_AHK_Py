# Auto_DAN3D_AHK_Py

creator:			Enok Cheon
date:			    2019-06-04
programming:	Python,	AutoHotKey(AHK)
License:			MIT License
Purpose:			automate DAN3D simulation and determine the barrier location

File Description:

'00 brief description.txt':	overall summary of project and file description

'00 explanation of dn3 file.txt':	explanation of dn3 file

'01_dan3d_input.csv':	input for DAN3D automation 
	- Each column represents each DAN3D file (dn3)
	- Input parameter on each row
	- If the number of soil material is bigger than one (1), another column is used

'02_create_dn3_files.py':	generate DAN3D file (dn3 file)
	- generate DAN3D input file (dn3 file), folder to store output, dn3 file name

'03_dn3_file_names_...xlsx':	excel file to open for autohotkey automation

'04_automate_dan3d_20190604.ahk':	automate DAN3D analysis
	- must have the appropriate button image saved
