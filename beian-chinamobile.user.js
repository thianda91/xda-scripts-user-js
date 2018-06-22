// ==UserScript==
// @name			Xianda-中国移动网站备案管理系统优化
// @description		本脚本用于beian.chinamobile.com界面优化。1.美化UI，响应式布局，消灭滚动条。2.整合为单页应用，无刷新查询，无跳转实现批量上传（左下角）。3.后续会增加自动化功能，新增或修改后自动上报。
// @author			Xianda
// @create			2018-06-10
// @version			0.3.3
// @match			*://beian.chinamobile.com/*
// @namespace		beian-chinamobile
// @license			MIT
// @copyright		2018, Xianda
// @lastmodified	2018-06-22
// @feedback-url	https://greasyfork.org/zh-CN/scripts/369426
// @note			2018-06-21-V0.3.2	修复bug
// @note			2018-06-19-V0.2.0	测试脚本无法自动更新
// @note			2018-06-13-V0.1.7	修复bug
// @note			2018-06-13-V0.1.5	调整布局，查询错误时支持显示错误提示
// @note			2018-06-13-V0.1.4	首页提示脚本启用，新增防掉线功能，修复若干bugs
// @note			2018-06-12-V0.1.3	显示退出按钮
// @note			2018-06-12-V0.1.2	更新 Userscript Header
// @note			2018-06-11-V0.1.1	支持记录本地登陆信息
// @note			2018-06-10-V0.1.0	支持查询
// @homepage		https://github.com/yuxianda/beian-chinamobile
// @icon			http://wx2.sinaimg.cn/large/679a709ely1frs5u2z5ibj205c05c3yd.jpg
// @downloadURL		https://greasyfork.org/scripts/369426-xianda-%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8%E7%BD%91%E7%AB%99%E5%A4%87%E6%A1%88%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%E4%BC%98%E5%8C%96/code/Xianda-%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8%E7%BD%91%E7%AB%99%E5%A4%87%E6%A1%88%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%E4%BC%98%E5%8C%96.user.js
// @run-at			document-body
// @grant			none
// ==/UserScript==

(function() {
	'use strict';

	var devVersion = "0.3.3";

	// Ajax 特效
	$("body").append('<style>.head{background:#94aedb}#load{position:absolute;top:0;bottom:0;left:0;right:0;z-index:200;}#load ._close{position:absolute;bottom:20px;left:0;height:50px;width:50px;font-size:100px;color:#000;cursor:pointer;line-height:50px;opacity:.2}.spinner{position:absolute;top:50%;left:50%;margin-top:-100px;margin-left:-300px;text-align:center}.spinner>div{width:200px;height:200px;background-color:#67CF22;border-radius:100%;display:inline-block;-webkit-animation:bouncedelay 1.4s infinite ease-in-out;animation:bouncedelay 1.4s infinite ease-in-out;-webkit-animation-fill-mode:both;animation-fill-mode:both}.spinner .bounce1{-webkit-animation-delay:-.32s;animation-delay:-.32s}.spinner .bounce2{-webkit-animation-delay:-.16s;animation-delay:-.16s}@-webkit-keyframes bouncedelay{0%,80%,100%{-webkit-transform:scale(0)}40%{-webkit-transform:scale(1)}}@keyframes bouncedelay{0%,80%,100%{transform:scale(0);-webkit-transform:scale(0)}40%{transform:scale(1);-webkit-transform:scale(1)}}</style><div id="load"><div class="_close" onclick="document.getElementById(&quot;load&quot;).style.display=&quot;none&quot;">×</div><div class="spinner"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div></div>');
	$(document).ajaxStart(function() {
		$("#load").show();
	}).ajaxStop(function() {
		$("#load").hide();
	});

	$(function() {
		$("#load").hide();

		// 首页
		if (document.myform && myform.action.match("/user/login.jhtml")) {
			//$("td[colspan=3]:first").removeAttr("colspan").after("<td colspan=2><b style='color:green'>已启用优化，登录后享受！</b></td>");
			//$("table table table tr:eq(1)").append("<td>V"+devVersion+"</td>");
			$("a.more").after('<div style="float:right;color:#fff;background-color:#000;margin-right:160px;padding:0 10px;">已启动优化,登录后查看！(V'+devVersion+')</div>')
			myform.userType.value = 2;
			window.myclick = function() {
				localStorage.setItem("xda_username", myform.userName.value);
				localStorage.setItem("xda_password", myform.password.value);
				var password = $("#password");
				var count = $("#count");
				if (count.val() == "") {
					password.val($.md5(password.val()));
				}
				return;
			}
			var username = localStorage.getItem("xda_username");
			var password = localStorage.getItem("xda_password");
			if (username && password) {
				login(username, password);
			}
			myform.authCode.value="";
			myform.authCode.focus();
			return;
		}

		// 自动跳转到查询页
		if (location.href.match("//beian.chinamobile.com/ismmobile/index/index.jhtml")) {
			location.href = "/ismmobile/ipbak/fp_xx_list.jhtml";
			return;
		}

		// 登录函数，本地自动登录
		function login(username, password) {
			myform.userName.value = username;
			myform.password.value = password;
		}

		// 移除header
		//document.getElementById("Container").style.marginTop = 0;
		//document.getElementsByClassName("header")[0].style.display = "none";
		document.getElementById("Container").style.marginTop = "70px";
		document.getElementsByClassName("header")[0].style.zIndex = "-1";

		// 隐藏左侧菜单
		document.getElementById("NavBar").style.display = "none";

		// 扩展显示主div到左侧边缘
		document.getElementById("MainBody").style.marginLeft = 0;

		// 去除子标题
		document.getElementsByClassName("subtitle")[0].style.display = "none";

		// 若不是查询页则结束执行
		if(!location.href.match("ipbak/fp_xx_list.jhtml")){
			return;
		}

		// ip查询页(fp_xx_list.jhtml) 隐藏不常用的条件输入框
		//if(location.pathname.indexOf("ismmobile/ipbak/fp_xx_list.jhtml")>0){
		var __uselessLine = [0, 2, 5, 6, 7];
		for (var i in __uselessLine) {
			$("#major-content table.t-detail tr:eq(" + __uselessLine[i] + ")").hide();
		}

		// 调整 查询表单 的位置
		$("#major-content table.t-detail tr:eq(1) td:eq(1)").append($("#major-content table.t-detail tr:eq(1) td:eq(2)").text()).append($("#major-content table.t-detail tr:eq(1) td:eq(3) select"));
		$("#major-content table.t-detail tr:eq(1) td:eq(2)").html('<span style="color: #088bff;font-size: 14px;">UI优化：<a href="https://github.com/yuxianda" target="_blank">Xianda</a></span>');
		//$("#major-content table.t-detail tr:eq(1) td:eq(3)").html($(".header .user").html());
		//$("#major-content table.t-detail tr:eq(1) td:eq(3) .exit").css({"background":"url(../../images/v3/exit.gif) no-repeat","padding-left":"20px","color":"#102c93","margin":"0 20px"});
		//$("#major-content table.t-detail tr:eq(1) td:eq(3)").css("text-align", "right");
		$("#major-content table.t-detail tr:eq(4) td:eq(3)").html('Version: ' + devVersion);

		// 添加提示
		$("#major-content table.t-detail tr:eq(4) td:eq(1)").html($("#major-content table.t-detail tr:eq(4) td:eq(1)").html().replace('格式：192.168.1.1', '<span style="color:red">结束ip留空，查询时会自动和起始ip相同</span>'));
		$("#major-content table.t-detail tr:eq(4) td:eq(2)").text("");

		// 取消搜索结果div的宽度限制
		adjustDataTable();

		// 添加批量操作功能到当前页
		$("#MainBody div:last").prepend('<div id="XiandaDiv" style="display: inline-block; float: left; width: 750px;"></div>');
		$("#XiandaDiv").load("batch_fpxx_new.jhtml .yui-g",function(){
			$("#XiandaDiv").html($("#XiandaDiv").html().replace(/批量/g,""));
			// 导入操作从新窗口打开
			fp_xx_new_fm.target="_blank";
			// 导入函数
			window.mysumitAdd = function(){
				var file= document.fp_xx_new_fm.file2.value;
				if (file!=""&&file!=null){
					document.fp_xx_new_fm.submit();
				}
				else{
					alert("未选导入文件");
				}
			}
			//$("#XiandaDiv a:last").text("验证文件下载");
		});

		// 隐藏上方的批量操作按钮
		$("#major-content table tr:eq(8) td.value input")[2].style.display = "none";

		// 防掉线
		$("#major-content form[name='qvo_fm'] td:last").prepend('<button id="prevDown" class="button" data-txt="no">开启防掉线</button>');
		$("#prevDown").bind("click",function(){
			var tpl = {no:['yes','关闭防掉线'],yes:['no','开启防掉线']};
			var _status = $(this).attr("data-txt");
			if(_status=='no'){
				flip(this);
			}else if(_status=='yes'){
				clearTimeout(this.flip);
			}
			$(this).text(tpl[_status][1]);
			$(this).attr("data-txt",tpl[_status][0]);
			return false;
		});

		// 删除 fp_xx_delete

		// 上报 fp_xx_upload


	});

	// 随机setInterval函数
	window.flip = function(obj){
		var timeout=Math.round(Math.random()*60000+40000);
		clearTimeout(obj.flip);
		obj.flip=setTimeout(function timeoutFun(){
			$.get("/ismmobile/index/index.jhtml");
			timeout=Math.round(Math.random()*60000+40000);
			obj.flip=setTimeout(timeoutFun,timeout);
		},timeout);
	}

	// 调整查询结果的表格大小
	window.adjustDataTable = function(){
		document.getElementById("data_table").width = "100%";
		del_fm.childNodes[3].style.width = "";
		var _htmlHeight = document.documentElement ? document.documentElement.clientHeight : document.body.clientHeight;
		del_fm.style.height = _htmlHeight - 70 - qvo_fm.clientHeight - 55 - 33 - 20 - 10 + "px";
	}

	// 替换默认的查询功能为无刷新查询
	window.querysubmit = function() {
		//xda_search(document.getElementById());
		if(FormIsValid() == false) return;
		// 自动补全 ipStr_end
		if(qvo_fm.ipStr_end.value == "") qvo_fm.ipStr_end.value = qvo_fm.ipStr_begin.value;
		// 添加参数，使单页最多显示1000条查询结果
		$("#major-content table.t-detail tr:eq(7)").append('<td></td><td><input name="pSize" value="200"></td>');
		if(document.resultform) resultform.pSize.value = 200;
		var searchUrl = "http://beian.chinamobile.com/ismmobile/ipbak/fp_xx_list.jhtml #MainBody";
		if(document.getElementById("xda_temp")==undefined) $("body").append('<div id="xda_temp" style="display:none;"></div>');
		$("#xda_temp").load(searchUrl,serializeForm(qvo_fm),function(data){
			//var noticeReg = /\('NoticeBox[12]'\)" class="close">\[X\]<\/span><p style="text-align:left;">(.+)<b/;
			var xda_data = data.replace(/[\t\r\n]/g,"");
			window.aaa=xda_data;
			var result = xda_data.match(/<div id="NoticeBox.+<\/p><\/div>/);
			if(result){
				$("#major-content").before(result[0]);
				$(".msg-box").css({"position":"absolute","left":"480px","top":"10px","width":"350px"});
			}else{
				$("#Main #major-content form[name='del_fm']").replaceWith($("#xda_temp form[name='del_fm']"));
				$("#Main #major-content #page form").replaceWith($("#xda_temp #page form"));
				setTimeout(adjustDataTable,0);
			}
			$("#xda_temp").remove();
		});

		/*var searchUrl = "http://beian.chinamobile.com/ismmobile/ipbak/fp_xx_list.jhtml form[name='del_fm'] div";
		$("form[name='del_fm']").load(searchUrl, serializeForm(qvo_fm), function() {
			document.getElementById("data_table").width = "100%";
			del_fm.childNodes[1].style.width = "";
		});*/
	}

	// 替换默认的查询功能为无刷新查询
	window.querysubmit = function() {

	}

	// 替换默认的查询功能为无刷新查询
	window.querysubmit = function() {

	}
	// 替换默认的查询功能为无刷新查询
	window.querysubmit = function() {

	}

	//获取指定form中的所有的<input>对象
	window.getElements = function(formId) {
		//var form = document.getElementById(formId);
		var form = formId;
		var elements = new Array();
		var tagElements = form.getElementsByTagName('input');
		for (var j = 0; j < tagElements.length; j++) {
			elements.push(tagElements[j]);
		}
		var tagElements2 = form.getElementsByTagName('select');
		for (var j2 = 0; j2 < tagElements2.length; j2++) {
			elements.push(tagElements2[j2]);
		}
		var tagElements3 = form.getElementsByTagName('textarea');
		for (var j3 = 0; j3 < tagElements3.length; j3++) {
			elements.push(tagElements3[j3]);
		}
		return elements;
	}

	//组合URL
	window.serializeElement = function(element) {
		var method = element.tagName.toLowerCase();
		var parameter;
		if (method == 'select') {
			parameter = [element.name, element.value];
		}
		switch (element.type.toLowerCase()) {
			case 'submit':
			case 'hidden':
			case 'password':
			case 'text':
			case 'date':
			case 'textarea':
				parameter = [element.name, element.value];
				break;
			case 'checkbox':
			case 'radio':
				if (element.checked) {
					parameter = [element.name, element.value];
				}
				break;
		}
		if (parameter) {
			var key = encodeURIComponent(parameter[0]);
			if (key.length == 0) return;
			if (parameter[1].constructor != Array) parameter[1] = [parameter[1]];
			var values = parameter[1];
			var results = [];
			for (var i = 0; i < values.length; i++) {
				results.push(key + '=' + encodeURIComponent(values[i]));
			}
			return results.join('&');
		}
	}

	//调用方法
	window.serializeForm = function(formId) {
		var elements = getElements(formId);
		var queryComponents = new Array();
		for (var i = 0; i < elements.length; i++) {
			var queryComponent = serializeElement(elements[i]);
			if (queryComponent) {
				queryComponents.push(queryComponent);
			}
		}
		return queryComponents.join('&');
	}
})();
