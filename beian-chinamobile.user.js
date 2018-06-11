// ==UserScript==
// @name			Xianda-移动集团工信部ip备案系统优化
// @description		Beautify the web UI, simplify the functions. Do less, work out more! Who try who knows.
// @author			Xianda
// @create			2018-06-10
// @version		 	0.1.2
// @match			*://beian.chinamobile.com/*
// @namespace		yuxianda.tl@139.com
// @copyright		2018, Xianda
// @lastmodified	2018-06-12
// @feedback-url	https://greasyfork.org/zh-CN/scripts/369426
// @note			2018-06-12-V0.1.2	更新 Userscript Header
// @note			2018-06-11-V0.1.1	支持记录本地登陆信息
// @note			2018-06-10-V0.1.0	支持查询
// @homepage		https://github.com/yuxianda/beian-chinamobile
// @icon			http://wx2.sinaimg.cn/large/679a709ely1frs5u2z5ibj205c05c3yd.jpg
// @downloadURL		https://greasyfork.org/scripts/369426/code/Xianda-%E7%A7%BB%E5%8A%A8%E9%9B%86%E5%9B%A2%E5%B7%A5%E4%BF%A1%E9%83%A8ip%E5%A4%87%E6%A1%88%E7%B3%BB%E7%BB%9F%E4%BC%98%E5%8C%96.user.js
// @run-at			document-body
// @grant			none
// ==/UserScript==

(function() {
	'use strict';

	var devVersion = "0.1.2";

	// Ajax 特效
	$("body").append('<style>#load{position:absolute;top:0;bottom:0;left:0;right:0;z-index:200;display:none}#load ._close{position:absolute;bottom:20px;left:0;height:50px;width:50px;font-size:100px;color:#000;cursor:pointer;line-height:50px;opacity:.2}.spinner{position:absolute;top:50%;left:50%;margin-top:-100px;margin-left:-300px;text-align:center}.spinner>div{width:200px;height:200px;background-color:#67CF22;border-radius:100%;display:inline-block;-webkit-animation:bouncedelay 1.4s infinite ease-in-out;animation:bouncedelay 1.4s infinite ease-in-out;-webkit-animation-fill-mode:both;animation-fill-mode:both}.spinner .bounce1{-webkit-animation-delay:-.32s;animation-delay:-.32s}.spinner .bounce2{-webkit-animation-delay:-.16s;animation-delay:-.16s}@-webkit-keyframes bouncedelay{0%,80%,100%{-webkit-transform:scale(0)}40%{-webkit-transform:scale(1)}}@keyframes bouncedelay{0%,80%,100%{transform:scale(0);-webkit-transform:scale(0)}40%{transform:scale(1);-webkit-transform:scale(1)}}</style><div id="load"><div class="_close" onclick="document.getElementById(&quot;load&quot;).style.display=&quot;none&quot;">×</div><div class="spinner"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div></div>');
	$(document).ajaxStart(function() {
		$("#load").show();
	}).ajaxStop(function() {
		$("#load").hide();
	});

	if (document.myform && myform.action.match("/user/login.jhtml")) {
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
		return;
	}
	if (location.href.match("//beian.chinamobile.com/ismmobile/index/index.jhtml")) {
		location.href = "/ismmobile/ipbak/fp_xx_list.jhtml";
		return;
	}

	// 登录函数，本地自动登录
	function login(username, password) {
		myform.userName.value = username;
		myform.password.value = password;
	}

	$(function() {

		// 移除header
		document.getElementById("Container").style.marginTop = 0;
		document.getElementsByClassName("header")[0].style.display = "none";

		// 隐藏左侧菜单
		document.getElementById("NavBar").style.display = "none";

		// 扩展显示主div到左侧边缘
		document.getElementById("MainBody").style.marginLeft = 0;
		// 去除子标题
		document.getElementsByClassName("subtitle")[0].style.display = "none";

		// ip查询页(fp_xx_list.jhtml) 隐藏不常用的条件输入框
		//if(location.pathname.indexOf("ismmobile/ipbak/fp_xx_list.jhtml")>0){
		var __uselessLine = [0, 2, 5, 6, 7];
		for (var i in __uselessLine) {
			$("#major-content table tr:eq(" + __uselessLine[i] + ")").hide();
		}

		// 调整 备案状态 选项的位置
		$("#major-content table tr:eq(1) td:eq(1)").append($("#major-content table tr:eq(1) td:eq(2)").text());
		$("#major-content table tr:eq(1) td:eq(1)").append($("#major-content table tr:eq(1) td:eq(3) select"));
		$("#major-content table tr:eq(1) td:eq(2)").html('<span style="color: #088bff;font-size: 14px;">UI优化：<a href="https://github.com/yuxianda" target="_blank">Xianda</a></span>');
		$("#major-content table tr:eq(1) td:eq(3)").html('Version: ' + devVersion);
		$("#major-content table tr:eq(1) td:eq(3)").css("padding-left", "100px");

		// 添加提示
		$("#major-content table tr:eq(4) td:eq(1)").html($("#major-content table tr:eq(4) td:eq(1)").html().replace('格式：192.168.1.1', '<span style="color:red">结束ip留空，查询时会自动和起始ip相同</span>'));
		$("#major-content table tr:eq(4) td:eq(2)").text("");
		$("#major-content table tr:eq(4) td:eq(3)").text("");

		// 添加参数，使单页最多显示1000条查询结果
		$("#major-content table tr:eq(7)").append('<td></td><td><input name="pSize" value="1000"></td>');
		resultform.pSize.value = 1000;

		// 取消搜索结果div的宽度限制
		document.getElementById("data_table").width = "100%";
		del_fm.childNodes[3].style.width = "";
		var _htmlHeight = document.documentElement ? document.documentElement.clientHeight : document.body.clientHeight;
		del_fm.style.height = _htmlHeight - qvo_fm.clientHeight - 55 - 33 - 20 - 10 + "px";

		// 添加批量操作功能到当前页
		$("#MainBody div:last").prepend('<div id="XiandaDiv" style="display: inline-block; float: left;"></div>');
		$("#XiandaDiv").load("batch_fpxx_new.jhtml .yui-g");

		// 隐藏上方的批量操作按钮
		$("#major-content table tr:eq(8) td.value input")[2].style.display = "none";

		// 替换默认的查询功能为无刷新查询
		function querysubmit() {
			//xda_search(document.getElementById());
			if (FormIsValid() == false) {
				return;
			}
			// 自动补全 ipStr_end
			if (qvo_fm.ipStr_end.value == "") {
				qvo_fm.ipStr_end.value = qvo_fm.ipStr_begin.value;
			}
			var searchUrl = "http://beian.chinamobile.com/ismmobile/ipbak/fp_xx_list.jhtml form[name='del_fm'] div";
			$("form[name='del_fm']").load(searchUrl, serializeForm(qvo_fm), function() {
				document.getElementById("data_table").width = "100%";
				del_fm.childNodes[1].style.width = "";
			});
		}

		//获取指定form中的所有的<input>对象
		function getElements(formId) {
			//var form = document.getElementById(formId);
			var form = formId;
			var elements = new Array();
			var tagElements = form.getElementsByTagName('input');
			for (var j = 0; j < tagElements.length; j++) {
				elements.push(tagElements[j]);
			}
			var tagElements2 = form.getElementsByTagName('select');
			for (var j2 = 0; j2 < tagElements2.length; j++) {
				elements.push(tagElements2[j3]);
			}
			var tagElements3 = form.getElementsByTagName('textarea');
			for (var j3 = 0; j3 < tagElements3.length; j++) {
				elements.push(tagElements3[j3]);
			}
			return elements;
		}
		
		//组合URL
		function serializeElement(element) {
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
		function serializeForm(formId) {
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

	});
})();