# Auto_DAN3D_AHK_Py
Creator:	Enok Cheon   
Date:		2021-06-08 (originally 2019-06-04)   
Programming:	Python,	AutoHotKey(AHK)   
License:	MIT License   
Purpose:	automate DAN3D simulation and determine the barrier location   

Preparation:   
- prepare all the input DEM files required for DAN3D analysis   
- save all the input DEM and the download files into one single folder
- no spacing in file names and only English folder or folderpath names
- using text editor (sublime text or vs-code) would be adviced   

File Description:

'00 explanation of dn3 file.txt':   
- explanation of dn3 file format   

'01_dan3d_input.csv':   
- input for DAN3D automation   
- Each column represents each DAN3D file (dn3)   
- Input parameter on each row   
- If the number of soil material is bigger than one (1), another column is used   

'02_create_dn3_files.py':   
- generate DAN3D file (dn3 file)   
- generate DAN3D input file (dn3 file), folder to store output, dn3 file name   
- must install xlsxwriter python library   

'03_dn3_file_names_...xlsx':   
- excel file to open for autohotkey automation   

'04_automate_dan3d.ahk':   
- automate DAN3D analysis   
- must write DAN3D.exe full file location (line 17)    
- must have the appropriate button image captured and saved (line 25 and 39)   
