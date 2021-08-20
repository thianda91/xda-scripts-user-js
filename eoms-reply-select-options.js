//
// EOMS 故障处理工单(设备) 自动回单脚本
// 在IE9下，工单详细页按F12调试，点击控制台面板
// 直接复制粘贴底部的压缩版本即可。
// 一键回单
// Author X.Da
// version 3.0
//

var $o = function(arg) {return document.getElementById(arg);};
if ($o('BaseSummary').value.indexOf('事件') != -1 && $o('AlarmLevel').value == '三级告警') {
    $o('bpp_Btn_T1Finish').click();
    setTimeout(function(){
        F('DealDesc').S('已知晓');
    },1000);
} else {
	// 点击完成处理 按钮
	// $o("bpp_Btn_ACCEPT")&&$o("bpp_Btn_ACCEPT").click();
	// $o("bpp_ActPanel").currentStyle.display=="none"&&$o("bpp_Btn_T2Finish").click();
	$o("bpp_Btn_T2Finish").click();
	// 点击完成处理按钮后延时填写
	setTimeout(function() {
		window.scrollTo(0, 5000);
		var _boolean = F("ClearINCTime").G()=="";
		if (_boolean) {
			alert('不要回单！\n没有上清除时间，看好咯！')
		};	
		else {
			function sc(){
				F("tth_region").S("农村");
				F("ReasonType").S("数通设备");
				F("ReasonSubType").S("传输原因");
				F("FinishDealDesc").S("传输链路闪断造成");
				F("DealGuomodo").S("检查线路传输质量");
				F("isHomeService").S("否");
				F("fault_recover").S("彻底恢复");
			}
			function dev(){
				F("tth_region").S("农村");
				F("ReasonType").S("数通设备");
				F("ReasonSubType").S("设备原因");
				F("FinishDealDesc").S("内存占用率过高");
				F("DealGuomodo").S("清除冗余内存"); 
				F("isHomeService").S("否");
				F("fault_recover").S("彻底恢复");
			}
			function func_lost(){
				F("tth_region").S("农村");
				F("ReasonType").S("数通设备");
				F("ReasonSubType").S("设备原因");
				F("FinishDealDesc").S("防尘网需清洗");
				F("DealGuomodo").S("清洗防尘网"); 
				F("isHomeService").S("是");
				F("fault_recover").S("彻底恢复");
			}
			function manual(){
				F("tth_region").S("农村");
				F("ReasonType").S("数通设备");
				F("ReasonSubType").S("其他原因");
				F("FinishDealDesc").S("手动down");
				F("DealGuomodo").S("手动down"); 
				F("isHomeService").S("是");
				F("fault_recover").S("彻底恢复");
			}
			function optical(){
				F("tth_region").S("农村");
				F("ReasonType").S("数通设备");
				F("ReasonSubType").S("设备原因");
				F("FinishDealDesc").S("光模块松动或故障"); // 填写你的自定义故障原因
				F("DealGuomodo").S("更换光模块"); // 填写你的自定义处理措施
				F("isHomeService").S("是");
				F("fault_recover").S("彻底恢复");
			}
			function porj(){
				F("tth_region").S("农村");
				F("ReasonType").S("数通设备");
				F("ReasonSubType").S("工程操作");
				F("FinishDealDesc").S("工程遗留");
				F("DealGuomodo").S("维护人员确认后解决"); 
				F("isHomeService").S("否");
				F("fault_recover").S("彻底恢复");
			}
			sc();
		}
	ActionPanel.submit();
	}, 1000);
}

// **为方便在IE9浏览器的调试模式执行。可使用压缩版本（单行），直接复制粘贴运行

// 传输原因：
var $o=function(arg){return document.getElementById(arg);};$o("bpp_Btn_T2Finish").click();setTimeout(function(){window.scrollTo(0,5000);var _boolean=F("ClearINCTime").G()=="";if(_boolean){alert('不要回单！\n没有上清除时间，看好咯！')}	else{F("tth_region").S("农村");F("ReasonType").S("数通设备");F("ReasonSubType").S("传输原因");F("FinishDealDesc").S("传输链路闪断造成");F("DealGuomodo").S("检查线路传输质量");F("isHomeService").S("否");F("fault_recover").S("彻底恢复");ActionPanel.submit();}},1000);
var $o=function(arg){return document.getElementById(arg);};if ($o('BaseSummary').value.indexOf('事件') != -1 && $o('AlarmLevel').value == '三级告警') {$o('bpp_Btn_T1Finish').click();setTimeout(function(){F('DealDesc').S('已知晓');},1000);}else{$o("bpp_Btn_T2Finish").click();setTimeout(function(){window.scrollTo(0,5000);var _boolean=F("ClearINCTime").G()=="";if(_boolean){alert('不要回单！\n没有上清除时间，看好咯！')}	else{F("tth_region").S("农村");F("ReasonType").S("数通设备");F("ReasonSubType").S("传输原因");F("FinishDealDesc").S("传输链路闪断造成");F("DealGuomodo").S("检查线路传输质量");F("isHomeService").S("否");F("fault_recover").S("彻底恢复");ActionPanel.submit();}},1000);}ActionPanel.submit();
var $o=function(arg){return document.getElementById(arg);};if ($o('BaseSummary').value.indexOf('事件') != -1 && $o('AlarmLevel').value == '三级告警') {$o('bpp_Btn_T1Finish').click();setTimeout(function(){F('DealDesc').S('已知晓');},1000);}else{$o("bpp_Btn_T2Finish").click();setTimeout(function(){window.scrollTo(0,5000);var _boolean=F("ClearINCTime").G()=="";if(_boolean){alert('不要回单！\n没有上清除时间，看好咯！')}	else{F("tth_region").S("农村");F("ReasonType").S("数通设备");F("ReasonSubType").S("传输原因");F("FinishDealDesc").S("传输链路闪断造成");F("DealGuomodo").S("检查线路传输质量");F("isHomeService").S("否");F("fault_recover").S("彻底恢复");}},1000);}
// 手动down：
var $o=function(arg){return document.getElementById(arg);};$o("bpp_Btn_T2Finish").click();setTimeout(function(){window.scrollTo(0,5000);var _boolean=F("ClearINCTime").G()=="";if(_boolean){alert('不要回单！\n没有上清除时间，看好咯！')}	else{F("tth_region").S("农村");F("ReasonType").S("数通设备");F("ReasonSubType").S("其他原因");F("FinishDealDesc").S("手动down");F("DealGuomodo").S("手动down");F("isHomeService").S("是");F("fault_recover").S("彻底恢复");ActionPanel.submit();}},1000);
// 工程遗留：
var $o=function(arg){return document.getElementById(arg);};$o("bpp_Btn_T2Finish").click();setTimeout(function(){window.scrollTo(0,5000);var _boolean=F("ClearINCTime").G()=="";if(_boolean){alert('不要回单！\n没有上清除时间，看好咯！')}	else{F("tth_region").S("农村");F("ReasonType").S("数通设备");F("ReasonSubType").S("工程操作");F("FinishDealDesc").S("工程遗留");F("DealGuomodo").S("维护人员确认后解决");F("isHomeService").S("否");	F("fault_recover").S("彻底恢复");ActionPanel.submit();}},1000);

// 在线工具： https://tool.lu/js/


// 事件，直接回单
// http://10.204.14.35/eoms4/sheet/myWaitingDealSheetQuery.action?baseSchema=WF4_EL_TTM_TTH_NOTICE&id=8a4c8ea376938d3d0176944e21980ab4
var $o = function(arg) {return document.getElementById(arg);};
if ($o('BaseSummary').value.indexOf('事件') != -1 && $o('AlarmLevel').value == '三级告警') {
    $o('bpp_Btn_T1Finish').click();
    setTimeout(function(){
        F('DealDesc').S('已知晓');
        ActionPanel.submit();
    },1000);
}

var $o = function(arg) {return document.getElementById(arg);};if ($o('BaseSummary').value.indexOf('事件') != -1 && $o('AlarmLevel').value == '三级告警') {$o('bpp_Btn_T1Finish').click();setTimeout(function(){F('DealDesc').S('已知晓');ActionPanel.submit();},1000);}