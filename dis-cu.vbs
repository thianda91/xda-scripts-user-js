#$language = "VBScript"
#$interface = "1.0"
crt.Screen.Synchronous = True '执行脚本结果同步显示到屏幕
	'1.参数定义。
	Const ForReading = 1, ForWriting = 2, ForAppending = 8
	Dim fso,logfile,fldr,tt,objNetwork,strUser
	linenum = 0
'
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set objNetwork = CreateObject("Wscript.Network")  
	strUser = objNetwork.UserName
	Dim rootDir
	rootDir	= "\\4A3-FTPTRANS01\ftptrans\" & strUser
	fldr = rootDir & "\_dis-cu\" & year(Now) & "-" & Month(Now) & "-" & day(Now) & " " & Weekdayname(Weekday(now))
	tt = fso.FolderExists(fldr)
	if tt<>true Then fso.CreateFolder(fldr)
	Dim the_ip
	the_ip=crt.Dialog.Prompt("Input for the log file name(tips: the ip or the description such as `bas02`):", "Enter IP or Name", "", false)
	logfile = fldr & "\" & the_ip & "-dis_cu-" & year(Now) & "-" & Month(Now) & "-" & day(Now) & ".txt"
	crt.Session.LogFileName = logfile
	crt.Session.Log(True)

	crt.Screen.Send vbcr
	crt.Screen.WaitForString ">"
	'【判断6】执行命令
	crt.Screen.Send chr(32) & "screen-length 0 temporary" & vbcr
	crt.Screen.Send chr(32) & " sys" & vbcr
	crt.Screen.Send vbcr & chr(32) & " dis cu"
	crt.sleep 1000
	crt.Screen.Send vbcr
	crt.sleep 1000
	do while (crt.Screen.waitforstrings("More","MORE","more",10)<>false) 
		crt.Screen.Send chr(32)
	loop
	crt.Screen.Send chr(32) & vbcr
	crt.Screen.Send chr(32) & " q" & vbcr
	crt.Screen.waitforstring ">"
	crt.Session.Log(false)
	setAuthor_v2 logfile
	'【判断6】登陆方式，并进一步退出

	crt.Screen.Send chr(32) & vbcr
	crt.Screen.Send chr(32) & " quit" 


	
'end Function

Function setAuthor(logfile)
	dim templog,temline
	set templog = fso.CreateTextFile("tmp.txt",True)
	templog.WriteLine "Scripts are powered by X.Da"
	templog.Close
	Set templog = fso.OpenTextFile("tmp.txt",1,False)
	temline =  templog.ReadLine
	templog.Close
	fso.deleteFile "tmp.txt"
	Dim thelog
	Set thelog = fso.OpenTextFile(logfile,8,False)
	thelog.WriteLine ""
	thelog.WriteLine temline & now '& " " & Weekdayname(Weekday(now))
	thelog.Close
end Function
Function setAuthor_v2(logfile)
	ConvertFile(logfile)
	Set thelog = fso.OpenTextFile(logfile,8,False)
	thelog.WriteLine ""
	dim msg
	msg="X.Da 采集于 "
	thelog.WriteLine msg & now & " " & Weekdayname(Weekday(now))
	thelog.Close
	'Set shell=createobject("wscript.shell")
	'a=shell.run("C:\a.bat " & logfile ,1)
end Function


'-------------------------------------------------

'函数名称:ReadFile

'作用:利用AdoDb.Stream对象来读取各种格式的文本文件

'-------------------------------------------------

 

Function ReadFile(FileUrl, CharSet)

    Dim Str

    Set stm = CreateObject("Adodb.Stream")

    stm.Type = 2

    stm.mode = 3

    stm.charset = CharSet

    stm.Open

    stm.loadfromfile FileUrl

    Str = stm.readtext

    stm.Close

    Set stm = Nothing

    ReadFile = Str

End Function

'-------------------------------------------------

'函数名称:WriteToFile

'作用:利用AdoDb.Stream对象来写入各种格式的文本文件

'-------------------------------------------------

 

Function WriteToFile (FileUrl, Str, CharSet)

    Set stm = CreateObject("Adodb.Stream")

    stm.Type = 2

    stm.mode = 3

    stm.charset = CharSet

    stm.Open

    stm.WriteText Str

    stm.SaveToFile FileUrl, 2

    stm.flush

    stm.Close

    Set stm = Nothing

End Function

'-------------------------------------------------

'函数名称:ConvertFile

'作用:将一个文件进行编码转换

'-------------------------------------------------

 

Function ConvertFile(FileUrl)

    Call WriteToFile(FileUrl, ReadFile(FileUrl, "utf-8"), "gb2312")

End Function