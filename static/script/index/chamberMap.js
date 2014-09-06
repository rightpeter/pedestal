
function moveElement(elementID,final_x,final_y,interval) {
  if (!document.getElementById) return false;
  if (!document.getElementById(elementID)) return false;
  var elem = document.getElementById(elementID);
  if (elem.movement) {          
    clearTimeout(elem.movement);
  }
  if (!elem.style.left) {
    elem.style.left = "-1600px";
  
  }
  if (!elem.style.top) {
    elem.style.top = "110px";

  }
  var xpos = parseInt(elem.style.left);
  var ypos = parseInt(elem.style.top);
  if (xpos == final_x && ypos == final_y) {
    return true;
  }
  if (xpos < final_x) {
    var dist = Math.ceil((final_x - xpos)/10);
    xpos = xpos + dist;
  }
  if (xpos > final_x) {
    var dist = Math.ceil((xpos - final_x)/10);
    xpos = xpos - dist;
  }
  if (ypos < final_y) {
    var dist = Math.ceil((final_y - ypos)/10);
    ypos = ypos + dist;
  }
  if (ypos > final_y) {
    var dist = Math.ceil((ypos - final_y)/10);
    ypos = ypos - dist;
  }
  elem.style.left = xpos + "px";
  elem.style.top = ypos + "px";
  var repeat = "moveElement('"+elementID+"',"+final_x+","+final_y+","+interval+")";
  elem.movement = setTimeout(repeat,interval);
}


function popChamberMap(){
  if (!document.getElementById) return false;
  if (!document.createElement) return false;
  if (!document.getElementById("svg")) return false;

  // 如果已经存在，先消除以前�?
  var SVG;
// alert(typeof(SVG));
  if ( document.getElementById("svgFile") != null ){
    SVG = document.getElementById("svg");
    var svgFile = document.getElementById("svgFile");
    SVG.removeChild(svgFile);
  }else{
    SVG = document.getElementById("svg");
    var svgFile = document.createElement("embed");
    svgFile.setAttribute("id","svgFile");
    svgFile.setAttribute("src","/static/buildings/1/1.svg");//这里写活
    svgFile.setAttribute("type","image/svg+xml");
    svgFile.setAttribute("width","780px");
    svgFile.setAttribute("height","500px");

    SVG.appendChild(svgFile);

    moveElement("chamberMap",0,110,10);
  }
}


// 弹出窗口回去
function goBack(){
  moveElement("chamberMap",-850,110,10);
  var SVG = document.getElementById("svg");
  var svgFile = document.getElementById("svgFile");
  SVG.removeChild(svgFile);
}

var init = function() {

    var latlngs = [
        new qq.maps.LatLng(39.086543,121.818034),//A
        new qq.maps.LatLng(39.085977,121.817398),//B
        new qq.maps.LatLng(39.086052,121.818573),//C
        new qq.maps.LatLng(39.082922,121.8181),//图书�?
        new qq.maps.LatLng(39.08468119272291,121.82072326540947),//食堂
      ];
    var srcs = [
        "/static/buildings/1/avator.jpg",
        "/static/buildings/50/avator.jpg",
        "/static/buildings/56/avator.jpg",
        "/static/buildings/57/avator.jpg",
        "/static/buildings/63/avator.jpg"
        ];
    map = new qq.maps.Map(document.getElementById('container'),{
        center: latlngs[3],
        zoom: 16
    });
    var infoWin = new qq.maps.InfoWindow({
        map: map
    });
    for(var i = 0;i < latlngs.length; i++) {
        (function(n){
          var marker = new qq.maps.Marker({
              map: map,
              position:latlngs[n],
              animation: qq.maps.MarkerAnimation.DROP
          });

          qq.maps.event.addListener(marker,'click',function(){
            popChamberMap();
            infoWin.open();
            infoWin.setContent('<div><img src= "'+srcs[n]+'"  style="width:100px;height:75px;"></div>');
                infoWin.setPosition(latlngs[n]);
          });

        })(i);
    }

}


