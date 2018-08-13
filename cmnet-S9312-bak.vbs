#$language = "VBScript"
#$interface = "1.0"
crt.Screen.Synchronous = True '执行脚本结果同步显示到屏幕
	'1.参数定义。
Dim fso
Set fso = CreateObject("Scripting.FileSystemObject")
start()
Function start()
	dim	right
	right = msgbox ("本脚本执行9312全局备份，请在BAS01上执行，BAS02运行本脚本会存在无法登录的9312。" & vbcr & vbcr & "确认请点击是，否则点击否" & vbcr & vbcr & "X.Da",4,"脚本使用说明")
	if right= 7 then exit function
	Dim objNetwork,strUser
	Set objNetwork = CreateObject("Wscript.Network")
	strUser = objNetwork.UserName
	Const ForReading = 1, ForWriting = 2, ForAppending = 8
	Dim filename
	filename = "\\10.204.205.236\4afile\"& strUser &"\_vbs\iptest.txt"
	Dim file1,file2,line,line2,linenum,params,params2,logfile,fldr,tt,jumpip,partemp
	linenum = 0
	
	Set file1 = fso.OpenTextFile(filename,Forreading, False)
	fldr = "\\10.204.205.236\4afile\"& strUser &"\_log\dis-cu\"&year(Now)&"-"&Month(Now)&"-"&day(Now)&" "&Weekdayname(Weekday(now))
	tt = fso.FolderExists(fldr)
	if tt<>true Then fso.CreateFolder(fldr)
	Dim tab
	DO While file1.AtEndOfStream <> True '循环读取每一行的IP信息
		line = file1.ReadLine
		params = Split (line)
		logfile = fldr & "\" & params(0) &".txt"
		crt.Session.LogFileName = logfile
		crt.Session.Log(True)
		crt.Screen.Send "telnet" & chr(32) & params(0) & chr(32) & vbcr 
		crt.Screen.WaitForString "sername:",2
		crt.Screen.Send params(1) & vbcr
		crt.Screen.waitforstring "assword:"
		crt.Screen.Send params(2) & vbcr
		crt.sleep 1000
		do while (crt.Screen.waitforstrings("assword:","ailed",2)<>false)
			Dim pwd
			pwd=crt.Dialog.Prompt("再次输入【"&params(0)&"】的登录密码:", "Enter Password", params(2), false)
			crt.Screen.Send pwd & vbcr
		loop
'		crt.Screen.WaitForStrings ">",2
		crt.Screen.Send vbcr
		crt.Screen.WaitForString ">"
		'【判断6】执行命令
		crt.Screen.Send vbcr & chr(32) & " dis cu"
		crt.sleep 1000
		crt.Screen.Send vbcr
		crt.sleep 1000
		do while (crt.Screen.waitforstrings("More","MORE","more",2)<>false) 
			crt.Screen.Send chr(32)
		loop
		crt.Screen.Send chr(32) & vbcr
		crt.Screen.waitforstring ">"

		'【判断6】登陆方式，并进一步退出

		crt.Screen.Send chr(32) & vbcr
		crt.Screen.Send chr(32) & " quit" & vbcr
		do while (crt.Screen.waitforstrings(">","]",2)<>false) 
			crt.Screen.Send chr(32)
		loop
		crt.Session.Log(false)
		setAuthor_v2 logfile

	loop
	
end Function

Function setAuthor(logfile)
	dim templog,temline
	set templog = fso.CreateTextFile("tmp.txt",True)
	templog.WriteLine "Scripts are powered by X.Da  啊"
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