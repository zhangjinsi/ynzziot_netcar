// 定义全局变量
var map, car, label, centerPoint, timer, point, index = 0, followChk, playBtn, pauseBtn, resetBtn;

//定义初始化函数
function initFunction() {
	$(document).ready(function() {
		ct = compareTime($("#ipt1").val(), $("#ipt2").val());
		if($("#ipt1").val() && $("#ipt2").val()) {
			var xmlHttpReq = $.post("/trackback/", $("#form1").serialize(), function(data) {
				// jsonObj为全局变量
				jsonObj = JSON.parse(data);
				var len = jsonObj.length;
				initGlobalVariable();
				if(len && ct != 0) {			
					// 百度地图功能
					map = new BMap.Map("allmap");
					map.centerAndZoom(new BMap.Point(jsonObj[0].longitude, jsonObj[0].latitude), 15);
					map.enableScrollWheelZoom();
					map.addControl(new BMap.NavigationControl());
					map.addControl(new BMap.ScaleControl());
					map.addControl(new BMap.OverviewMapControl({
						isOpen : true
					}));
					
					// 通过DrivingRoute创建一个驾车导航实例
					var driving = new BMap.DrivingRoute(map);
					driving.search(new BMap.Point(jsonObj[0].longitude, jsonObj[0].latitude), new BMap.Point(jsonObj[len - 1].longitude, jsonObj[len - 1].latitude));
					// 检索后的回调函数
					driving.setSearchCompleteCallback(function() {
						// 得到路线上的所有point，返回一个数组
						// getPath()返回路线的地理坐标点数组，points是一个全局数组
						points = driving.getResults().getPlan(0).getRoute(0).getPath();
						
						// 画面移动到起点和终点的中间
						var leng = points.length;
						centerPoint = new BMap.Point((points[0].lng + points[leng - 1].lng) / 2, (points[0].lat + points[leng - 1].lat) / 2);
						map.panTo(centerPoint);
						
						// 连接所有点
						map.addOverlay(new BMap.Polyline(points, {
							strokeColor : "blue",
							strokeWeight : 5,
							strokeOpacity : 0.1,
							enableMassClear : false
						}));
						
						// 显示小车子
						label = new BMap.Label("", {
							enableMassClear : false,
							offset : new BMap.Size(-20, -20)
						});

						// 图像标注的地理位置是points[0]
						car = new BMap.Marker(points[0]);

						car.setLabel(label);
						map.addOverlay(car);

						// 点亮操作按钮
						playBtn.disabled = false;
						resetBtn.disabled = false;
					});
				} else {
					if(ct == 100) {
						return ;
					} else {
						alert("没有查询到满足条件的数据！");						
					}
				}
			});
		} else {
			alert("请输入开始时间和结束时间！");
		}
	});
}

// 定义play()函数
function play() {
	playBtn.disabled = true;
	pauseBtn.disabled = false;
	initBtn.disabled = true;
	refreshBtn.disabled = true;
	selectBtn.disabled = true;
	 resetBtn.disabled = true;
	point = points[index];
	if (index >= 0&& index<points.length -1) {
		overLay = new BMap.Polyline([points[index], points[index+1]], {
			strokeColor : "green",
			strokeWeight : 5,
			strokeOpacity : 1,
			enableMassClear : true
		 });
		map.addOverlay(overLay);
	 }
	// 设置文本信息
	 label.setContent("车牌：" + jsonObj[0].device_number);
	 car.setPosition(point);
	 index++;
	 if (followChk.checked) {
		 map.panTo(point);
	 }
	 if (index < points.length) {
		 timer = window.setTimeout("play(" + index + ")", 400);
	 } else {
		playBtn.disabled = true;
		pauseBtn.disabled = true;
		selectBtn.disabled = false;
		refreshBtn.disabled = false;
		selectBtn.disabled = false;
		resetBtn.disabled = false;
		map.panTo(point);
	}

}

// 定义pause()函数
function pause() {
	playBtn.disabled = false;
	pauseBtn.disabled = true;
	initBtn.disabled = true;
	refreshBtn.disabled = false;
	selectBtn.disabled = false;
	if (timer) {
		window.clearTimeout(timer);
	}
}

// 定义reset()函数
function resetFunction() {
	followChk.checked = false;
	playBtn.disabled = false;
	pauseBtn.disabled = true;
	initBtn.disabled = false;
	refreshBtn.disabled = false;
	
	if (timer) {
		window.clearTimeout(timer);
	}
	index = 0;
	car.setPosition(points[0]);
	map.panTo(centerPoint);
	map.removeOverlay(overLay);
	map.clearOverlays();
	initFunction();
	map.addOverlay(car);
	label.setContent("车牌：" + jsonObj[0].serialnumber);
}

//定义compareTime()函数
function compareTime(st, et) {
	if(st < et) {
		return 1;
	} else {
		if($("#ipt1").val() && $("#ipt2").val()) {
			alert("开始时间不能大于等于结束时间！");
			return 100;			
		} else {
			return ;
		}
	}
}

// 定义初始化全局变量的函数
function initGlobalVariable() {
	// 为全局变量赋值
	followChk = document.getElementById("follow");
	playBtn = document.getElementById("playId");
	pauseBtn = document.getElementById("pauseId");
	resetBtn = document.getElementById("resetId");
	initBtn = document.getElementById("bt3");
	refreshBtn = document.getElementById("bt4");
	selectBtn = document.getElementById("selectId");
}
