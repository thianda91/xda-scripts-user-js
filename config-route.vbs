
'''˫�����Զ���ȡIPʱ��·���޸�


' Set WshShell = WScript.CreateObject("WScript.Shell")
' runn = "schtasks /create /sc MINUTE /mo 10 /ru System /tn config-route /tr """ & Wscript.ScriptFullName & """"
' msgbox(runn)
' WshShell.Exec(runn)
' WScript.Quit

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
					If dhcp = "��" Then
						' MsgBox("��ǰ����DHCP�Զ���ȡ���޷�ִ�У�" & vbCrLf & "�����޸�IP Ϊ�Զ���ȡ")
						currPath = createobject("Scripting.FileSystemObject").GetFolder(".").Path
						' MsgBox("���ű�����·����" & vbCrLf & currPath & vbCrLf & "�����Զ���")
						WshShell.Exec("explorer /select, " & Wscript.ScriptFullName)
						WScript.Quit
					End If
				End If
				If InStr(strLine, "����") > 0 OR InStr(strLine, "gateway") > 0 Then
					getway = Mid(strLine, InStr(strLine, ":") + 2)
				End If
			Next
		End If
	loop

	If getway = "" Then
		' MsgBox("��������Ϊ�գ�����")
		Exit sub
	Else
		WshShell.Exec("route delete 0.0.0.0 mask 0.0.0.0 10.61.214.1")
		' MsgBox("�������أ�"&getway&"������ɾ��")
	End If
End sub