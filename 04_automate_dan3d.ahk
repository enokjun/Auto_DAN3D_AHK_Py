; Input file location of EXCEL file containing names of DAN3D dn3 file to run
/*
InputBox, InputExcelLocation, Input Excel File Location
Run, %InputExcelLocation%
WinWait, dn3_file_names - Excel
Sleep, 333
*/
XL := ComObjActive("Excel.Application")
NumOfProject := XL.Application.ActiveSheet.UsedRange.Rows.Count
; Input file location for DAN3D program
; MsgBox, 0, , %NumOfProject%
; InputBox, DAN3DLocation, DAN3D program exe location
Loop, %NumOfProject%
{
    ; run DAN3D program
    ; %DAN3DLocation%
    Run, C:\Users\...\DAN3D_Rel-2.exe
    WinWait, Dynamic Analysis of Landslide Motion in Three Dimensions
    Sleep, 333
    ; find the open existing file button - loop until found
    Loop
    {
        CoordMode, Pixel, Window
        ; screen-shot of OpenAnExistingFile in DAN3D start screen
        ImageSearch, FoundX, FoundY, 0, 0, 1920, 1080, C:\Users\...\04_AHK_screenshots\DAN3D_OpenAnExistingFile_screenshot.png
        If ErrorLevel = 0
        	Click, %FoundX%, %FoundY% Left, 1
    }
    Until ErrorLevel = 0
    ; copy the file name of the dn3 project 
    nameIndexLocation := "A" . A_Index
    XL.Range(nameIndexLocation).Copy 
    Send, {LControl Down}{v}{LControl Up}{Enter}  
    Sleep, 2000
    Loop
    {
        CoordMode, Pixel, Window
        ; screen-shot of OpenAnExistingFile in DAN3D start screen
        ImageSearch, FoundX, FoundY, 0, 0, 1920, 1080, C:\Users\...\04_AHK_screenshots\DAN3D_Run_screenshot.png
        If ErrorLevel = 0
        	Click, %FoundX%, %FoundY% Left, 1
    }
    Until ErrorLevel = 0
    Sleep, 2000
    maxSimTimeIndexLocation := "B" . A_Index
    TotalTime := 7500*XL.Range(maxSimTimeIndexLocation).Value
    Sleep, %TotalTime%
    Send, {n}
    Sleep, 2000
    Send, {Enter}
    Sleep, 1000
    ; Send, {LAlt Down}{F4}{LAlt Up}
    ;Sleep, 500
    ;Send, {Enter}
    ; Sleep, 5000
}