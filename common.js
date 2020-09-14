// 4A防掉线：

if($==jQuery){window._cc=0;setInterval(function(){$.get("/page/resgroup/searchFrame.jsp",function(data){window._cc++;console.log('',(new Date()).toString().substr(11,9),window._cc)})},40000);}else{alert("没有 jQuery！");}
window.flip=function(obj,url){var timeout=Math.round(Math.random()*60000+40000);clearTimeout(obj.flip);obj.flip=setTimeout(function timeoutFun(){$.get(url);timeout=Math.round(Math.random()*60000+40000);obj.flip=setTimeout(timeoutFun,timeout);},timeout);};var ff={};flip(ff,"/page/resgroup/searchFrame.jsp");

// 综合资源管理系统防掉线

if($==jQuery){window._cc=0;setInterval(function(){$.get("/irms",function(data){window._cc++;console.log('',(new Date()).toString().substr(11,9),window._cc)})},40000);}else{alert("没有 jQuery！");}
http://rms.nmc.ln.cmcc:7002/irms

// ITOM 自动巡检接入

window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("vo_connType").value='telnet';
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("vo_user").value='lnnmc';
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("port").value='23';
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("pwd1").value='nsml1234';
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("pwd2").value='nsml1234';
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("vo.cueSymbol").value='>';
window.frames["contentFrame"].frames["parentFrameUserNameList"].parentUnixShells.cycTableAddRow('tableId');
window.frames["contentFrame"].frames["parentFrameUserNameList"].parentUnixShells.cycTableAddRow('tableId');
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("all").click();
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("row_0_2").childNodes[1].childNodes[0].value='su';
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("row_0_2").childNodes[2].childNodes[0].value=':';
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("row_0_3").childNodes[1].childNodes[0].value='Lnyd12345$$';
window.frames["contentFrame"].frames["parentFrameUserNameList"].document.getElementById("row_0_3").childNodes[2].childNodes[0].value='>';


window.frames["contentFrame"].frames["parentFrameUserNameList"].parentUnixShells.add('unixshell');


window.flip=function(obj,func){var timeout=Math.round(Math.random()*60000+40000);clearTimeout(obj.flip);obj.t=1;obj.flip=setTimeout(function timeoutFun(){func();timeout=Math.round(Math.random()*60000+40000);obj.flip=setTimeout(timeoutFun,timeout);obj.t++;console.log("**自定义脚本已执行:",obj.t,"次。")},timeout)};var ff={};flip(ff,function(){ResetTimer()});

window.flip=function(obj,func){
	var timeout=Math.round(Math.random()*60000+40000);
	clearTimeout(obj.flip);
	obj.t=1;
	obj.flip=setTimeout(
		function timeoutFun(){
			func();
			timeout=Math.round(Math.random()*60000+40000);
			obj.flip=setTimeout(timeoutFun,timeout);
			obj.t++;
			console.log("**自定义脚本已执行:",obj.t,"次。");
		},
	timeout);
};
var ff={};
flip(ff,function(){ResetTimer()});

