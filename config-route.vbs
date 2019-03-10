
'''双网卡自动获取IP时的路由修改


'Set WshShell = WScript.CreateObject("WScript.Shell")
'runn = "schtasks /create /sc MINUTE /mo 10 /ru System /tn config-route /tr """ & Wscript.ScriptFullName & """"
'msgbox(runn)
'WshShell.Exec(runn)
'WScript.Quit

call main
sub main()
	Set WshShell = WScript.CreateObject("WScript.Shell")
	Set oExec = WshShell.Exec("ipconfig.exe /all")
	Set oStdOut = oExec.StdOut
	Do Until oStdOut.AtEndOfStream
		strLine = oStdOut.ReadLine
		If InStr(strLine, "oa") > 0 Then
			For counter = 1 To 15 '
				strLine = oStdOut.ReadLine
				If InStr(strLine, "DHCP") > 0 Then
					dhcp = Mid(strLine, InStr(strLine, ":") + 2)
					If dhcp = "否" Then
						MsgBox("当前不是DHCP自动获取，无法执行！" & vbCrLf & "请先修改IP 为自动获取")
						currPath = createobject("Scripting.FileSystemObject").GetFolder(".").Path
						MsgBox("本脚本所在路径：" & vbCrLf & currPath & vbCrLf & "即将自动打开")
						WshShell.Exec("explorer /select, " & Wscript.ScriptFullName)
						WScript.Quit
					End If
				End If
				If InStr(strLine, "网关") > 0 OR InStr(strLine, "gateway") > 0 Then
					getway = Mid(strLine, InStr(strLine, ":") + 2)
				End If
			Next
		End If
	loop

	If getway = "" Then
		'MsgBox("内网网关为空，正常")
		Exit sub
	Else
		WshShell.Exec("route delete 0.0.0.0 mask 0.0.0.0 10.61.214.1")
		'MsgBox("内网网关："&getway&"，现已删除")
	End If
End sub