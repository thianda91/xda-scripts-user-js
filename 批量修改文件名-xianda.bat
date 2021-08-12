@echo off
setlocal EnableDelayedExpansion
rem 指定存放文件的目录
color 5f
title 批量改文件名-xianda制作
echo 批量修改文件名
echo.
echo         请把文件放入到一个目录内（不要和本脚本同一目录）
set /p FolderName=输入修改的文件所在的目录：
set /p new_prefix=输入新文件名的前缀：（后缀默认为txt）
set /a num=1
echo.>fail.txt
echo ,,【备注：】>>fail.txt
@echo 原文件名,新文件名,改名是否成功请查看下面的备注;无内容则修改成功>记录.txt
for /f "delims=\" %%a in ('dir /b /a-d /o-d %FolderName%') do (
 ren "%FolderName%\%%a" "%new_prefix%_!num!.txt" || (echo 文件 %%a 改名失败;>>fail.txt && set /a num-=1)
 echo %%a,%new_prefix%_!num!.txt>>记录.txt && set /a num+=1

)
echo.>>记录.txt
echo ,,说明：将上面内容复制到excel表格即可很方便的查看文件名修改的对应关系>>记录.txt
type fail.txt>>记录.txt
del fail.txt /s
type 记录.txt>%FolderName%\批量改名记录.csv
del 记录.txt /s
cls
echo 修改完毕，请查看修改的结果。
echo 操作记录保存在文件所在目录的 批量改名记录.csv 里
pause>nul