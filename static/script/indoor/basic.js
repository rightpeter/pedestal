var building_list = new Array(); 

$(document).ready(function() {
    
});

function addBuilding(name, lat, lng, id)
{
    //alert('addBuilding: name=' + name + ' lat=' + lat + ' lng=' + lng);
    var point = new BMap.Point(lng, lat);
    var label = new BMap.Label(name, {position: point});
    label.setTitle(name);
    label.addEventListener("click", function(){
        window.location.href='/app/indoor/map?bid='+id+'&level=1';
    });
    map.addOverlay(label);
}

function getBuildingDetail(bid)
{
    $.getJSON("http://pedestal.cn:3358/jsongetdetail?bid="+bid+"&callback=?", function(detail){
        //document.getElementById('js_debug_msg').innerHTML = detail['fid'];
        if ( detail['fid']==0 )
        {
            //alert('haha' + detail['name']);
            building_list.push(detail);
            addBuilding(detail['name'], detail['lat'], detail['lng'], detail['id']);
        }
        return detail
    })
}
