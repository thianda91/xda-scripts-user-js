//
// EOMS 故障处理工单(设备) 自动回单脚本
// 在IE9下，工单详细页按F12调试，点击控制台面板
// 直接复制粘贴底部的压缩版本即可。
// 一键回单
// Author X.Da
// version 2.0
//

var F = function(arg){
G: function(){return document.getElementById(arg).value;}
S: function(s){document.getElementById(arg).value=s;}
}
var $o = function(arg) {
		return document.getElementById(arg);
	};
// 点击完成处理 按钮
$o("bpp_Btn_ACCEPT")&&$o("bpp_Btn_ACCEPT").click();
$o("bpp_ActPanel").currentStyle.display=="none"&&$o("bpp_Btn_T2Finish").click();
// 点击完成处理按钮后延时填写
setTimeout(function() {
	// 滚动页面到最底部（点击完成处理后，页面内容变多，）
	window.scrollTo(0, 5000);
	var _boolean = F("ClearINCTime").G()=="";
	if (_boolean) {
		// 无清除时间自动添加为当前时间
		F("ClearINCTime").S((new Date()).pattern("yyyy-MM-dd hh:mm:ss"));
	};	
	// 可自定义回复规则
	function sc(){
		F("ReasonType").S("传输线路");
		F("ReasonSubType").S("传输线路故障");
		F("FinishDealDesc").S("光缆质量下降，导致性能值不在标准范围内");
		F("DealGuomodo").S("更换或修复故障纤芯后，故障恢复。");
		F("isHomeService").S("否");
	}
	function person(){
		F("ReasonType").S("人为");
		F("ReasonSubType").S("其他原因");
		F("FinishDealDesc").S("空闲端口");
		F("DealGuomodo").S("手动空闲端口关闭");
		F("isHomeService").S("否");
	}
	function device_error(){
		F("ReasonType").S("其他");
		F("ReasonSubType").S("其他原因");
		F("FinishDealDesc").S("设备故障");
		F("DealGuomodo").S("告警已自动恢复");
		F("isHomeService").S("否");
	}
	function other(){
		F("ReasonType").S("其他");
		F("ReasonSubType").S("其他原因");
		F("FinishDealDesc").S("告警自动恢复"); // 填写你的自定义故障原因
		F("DealGuomodo").S("告警已自动恢复"); // 填写你的自定义处理措施
		F("isHomeService").S("否");
	}
	// 写入回复
	person();
	// 点击提交按钮
	if(_boolean&&$o("AttachmentsList_tagDownloadTable").childNodes[1].childNodes[1].innerHTML.indexOf("无附件!")){
		if(confirm("确认无附件 提交？\n\n【确认】 提交，【取消】 返回")){
			ActionPanel.submit();
		}
	}else{
		ActionPanel.submit();
	}
}, 1000);

// **为方便在IE9浏览器的调试模式执行。可使用压缩版本（单行），直接复制粘贴运行

// 传输原因：
var $o=function(b){return document.getElementById(b)};$o("bpp_Btn_ACCEPT")&&$o("bpp_Btn_ACCEPT").click();"none"==$o("bpp_ActPanel").currentStyle.display&&$o("bpp_Btn_T2Finish").click();setTimeout(function(){window.scrollTo(0,5E3);var b=""==$o("ClearINCTime").value;if(b){var g=$o("ClearINCTime"),a=new Date,h=a.getFullYear(),c=a.getMonth()+1,d=a.getDate(),e=a.getHours(),f=a.getMinutes(),a=a.getSeconds();10>c&&(c="0"+c);10>d&&(d="0"+d);10>e&&(e="0"+e);10>f&&(f="0"+f);10>a&&(a="0"+a);g.value=h+"-"+c+"-"+d+" "+e+":"+f+":"+a}$o("ReasonType").value="\u4f20\u8f93\u7ebf\u8def";$o("ReasonSubType").value="\u4f20\u8f93\u7ebf\u8def\u6545\u969c";$o("FinishDealDesc").value="\u5149\u7f06\u8d28\u91cf\u4e0b\u964d\uff0c\u5bfc\u81f4\u6027\u80fd\u503c\u4e0d\u5728\u6807\u51c6\u8303\u56f4\u5185";$o("DealGuomodo").value="\u66f4\u6362\u6216\u4fee\u590d\u6545\u969c\u7ea4\u82af\u540e\uff0c\u6545\u969c\u6062\u590d\u3002";$o("isHomeService").value="\u5426";b&&$o("AttachmentsList_tagDownloadTable").childNodes[1].childNodes[1].innerHTML.indexOf("\u65e0\u9644\u4ef6!")?confirm("\u786e\u8ba4\u65e0\u9644\u4ef6 \u63d0\u4ea4\uff1f\n\n\u3010\u786e\u8ba4\u3011 \u63d0\u4ea4\uff0c\u3010\u53d6\u6d88\u3011 \u8fd4\u56de")&&ActionPanel.submit():ActionPanel.submit()},1E3);

// 人为施工
var $o=function(a){return document.getElementById(a)};$o("bpp_Btn_ACCEPT")&&$o("bpp_Btn_ACCEPT").click();"none"==$o("bpp_ActPanel").currentStyle.display&&$o("bpp_Btn_T2Finish").click();setTimeout(function(){window.scrollTo(0,5E3);var a=""==F("ClearINCTime").G();a&&F("ClearINCTime").S((new Date).pattern("yyyy-MM-dd hh:mm:ss"));F("ReasonType").S("\u4eba\u4e3a");F("ReasonSubType").S("\u5176\u4ed6\u539f\u56e0");F("FinishDealDesc").S("\u7a7a\u95f2\u7aef\u53e3");F("DealGuomodo").S("\u624b\u52a8\u7a7a\u95f2\u7aef\u53e3\u5173\u95ed");F("isHomeService").S("\u5426");a&&$o("AttachmentsList_tagDownloadTable").childNodes[1].childNodes[1].innerHTML.indexOf("\u65e0\u9644\u4ef6!")?confirm("\u786e\u8ba4\u65e0\u9644\u4ef6 \u63d0\u4ea4\uff1f\n\n\u3010\u786e\u8ba4\u3011 \u63d0\u4ea4\uff0c\u3010\u53d6\u6d88\u3011 \u8fd4\u56de")&&ActionPanel.submit():ActionPanel.submit()},1E3);

// 其他原因：
var $o=function(b){return document.getElementById(b)};$o("bpp_Btn_ACCEPT")&&$o("bpp_Btn_ACCEPT").click();"none"==$o("bpp_ActPanel").currentStyle.display&&$o("bpp_Btn_T2Finish").click();setTimeout(function(){window.scrollTo(0,5E3);var b=""==$o("ClearINCTime").value;if(b){var g=$o("ClearINCTime"),a=new Date,h=a.getFullYear(),c=a.getMonth()+1,d=a.getDate(),e=a.getHours(),f=a.getMinutes(),a=a.getSeconds();10>c&&(c="0"+c);10>d&&(d="0"+d);10>e&&(e="0"+e);10>f&&(f="0"+f);10>a&&(a="0"+a);g.value=h+"-"+c+"-"+d+" "+e+":"+f+":"+a}$o("ReasonType").value="\u5176\u4ed6";$o("ReasonSubType").value="\u5176\u4ed6\u539f\u56e0";$o("FinishDealDesc").value="\u544a\u8b66\u81ea\u52a8\u6062\u590d";$o("DealGuomodo").value="\u544a\u8b66\u5df2\u81ea\u52a8\u6062\u590d";$o("isHomeService").value="\u5426";b&&$o("AttachmentsList_tagDownloadTable").childNodes[1].childNodes[1].innerHTML.indexOf("\u65e0\u9644\u4ef6!")?confirm("\u786e\u8ba4\u65e0\u9644\u4ef6 \u63d0\u4ea4\uff1f\n\n\u3010\u786e\u8ba4\u3011 \u63d0\u4ea4\uff0c\u3010\u53d6\u6d88\u3011 \u8fd4\u56de")&&ActionPanel.submit():ActionPanel.submit()},1E3);

// 设备故障
var $o=function(b){return document.getElementById(b)};$o("bpp_Btn_ACCEPT")&&$o("bpp_Btn_ACCEPT").click();"none"==$o("bpp_ActPanel").currentStyle.display&&$o("bpp_Btn_T2Finish").click();setTimeout(function(){window.scrollTo(0,5E3);var b=""==$o("ClearINCTime").value;if(b){var g=$o("ClearINCTime"),a=new Date,h=a.getFullYear(),c=a.getMonth()+1,d=a.getDate(),e=a.getHours(),f=a.getMinutes(),a=a.getSeconds();10>c&&(c="0"+c);10>d&&(d="0"+d);10>e&&(e="0"+e);10>f&&(f="0"+f);10>a&&(a="0"+a);g.value=h+"-"+c+"-"+d+" "+e+":"+f+":"+a}$o("ReasonType").value="\u5176\u4ed6";$o("ReasonSubType").value="\u5176\u4ed6\u539f\u56e0";$o("FinishDealDesc").value="\u8bbe\u5907\u6545\u969c";$o("DealGuomodo").value="\u544a\u8b66\u5df2\u81ea\u52a8\u6062\u590d";$o("isHomeService").value="\u5426";b&&$o("AttachmentsList_tagDownloadTable").childNodes[1].childNodes[1].innerHTML.indexOf("\u65e0\u9644\u4ef6!")?confirm("\u786e\u8ba4\u65e0\u9644\u4ef6 \u63d0\u4ea4\uff1f\n\n\u3010\u786e\u8ba4\u3011 \u63d0\u4ea4\uff0c\u3010\u53d6\u6d88\u3011 \u8fd4\u56de")&&ActionPanel.submit():ActionPanel.submit()},1E3);

// 在线工具： https://tool.lu/js/