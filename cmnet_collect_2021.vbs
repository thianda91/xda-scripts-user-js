#$language = "VBScript"
#$interface = "1.0"
crt.Screen.Synchronous = True '执行脚本结果同步显示到屏幕
	'1.参数定义。
	' Dim objNetwork,strUser
	' Set objNetwork = CreateObject("Wscript.Network")  
	' strUser = objNetwork.UserName 
	Const ForReading = 1, ForWriting = 2, ForAppending = 8
	' Dim filename
	' filename ="\\10.204.205.236\4afile\"& strUser &"\_vbs\cmnet-collect2017.txt"
	Dim fso,logfile,fldr,tt,file1,params,logForderName
	Dim user,pwd,disArp,disCur,staticRoute
	user = "" # define the username yourself
	pwd = ""
	linenum = 0
	'定义执行的命令
	' disArp = array("arp","display arp all")
	' disCur = array("ipam","display cu")
	' disStaticRoute = array("staticRoute","display ip routing-table")
	
	Set fso = CreateObject("Scripting.FileSystemObject")
	' fldr = "\\10.204.205.236\4afile\"& strUser &"\_log\dis-cu\"&year(Now)&"-"&Month(Now)&"-"&day(Now)&" "&Weekdayname(Weekday(now))
	' createForder(fldr)
	' createForder(fldr & "\" & disArp(0))
	' createForder(fldr & "\" & disCur(0))
	' createForder(fldr & "\" & disStaticRoute(0))
	' Dim the_ip
	' the_ip=crt.Dialog.Prompt("输入该设备IP的末尾数:", "Enter IP", "", false)
	device_name = "Devices.txt"
	Set file1 = fso.OpenTextFile(device_name,Forreading, False)
	DO While file1.AtEndOfStream <> True '循环读取每一行的IP信息
		line = file1.ReadLine
		params = Split(line)
		if the_ip = params(0) then logForderName = params(1)
	LOOP
	RunScript(disArp)
	RunScript(disCur)
	RunScript(disStaticRoute)
	crt.Screen.Send vbcr
	crt.Screen.Send "    Finished..."
	crt.Screen.Send vbcr & vbcr & vbcr

Function RunScript(sc)
	Dim fldr2
	fldr2 = fldr & "\" & sc(0) & "\" & logForderName
	createForder(fldr2)
	logfile = fldr2 & "\" & sc(0) & "#001.cfg"
	crt.Session.LogFileName = logfile
	crt.Session.Log(True)
	crt.Screen.Send vbcr
	crt.Screen.WaitForString ">"
	crt.Screen.Send vbcr
	'【判断6】执行命令
	crt.Screen.Send chr(32) & sc(1) & vbcr
	crt.sleep 100
	do while (crt.Screen.waitforstrings("More","MORE","more",2)<>false) 
		crt.Screen.Send chr(32)
	loop
	crt.Screen.Send chr(32) & vbcr
	crt.Screen.waitforstring ">"
	crt.Session.Log(false)
	setAuthor_v2 logfile
end Function
	
	
	
Function createForder(fldr)
	Dim f_t,fso_t
	Set fso_t = CreateObject("Scripting.FileSystemObject")
	f_t = fso_t.FolderExists(fldr)
	if f_t<>true Then fso_t.CreateFolder(fldr)
end Function
	
'end Function

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
	'utf-8 转 gb2312
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