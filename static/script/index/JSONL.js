/**
 * Created by Scott on 2014/4/9.
 */

function BuildingService() {
    if(typeof BuildingService._initialized == "undefined") {
        BuildingService._initialized = true;
    }
}
BuildingService.PICPREFIX = "/static/buildings/";
BuildingService.PICPOSTFIX="/avator.jpg";
BuildingService.DETAILPREFIX="www.pedestal.cn:3358/getdetail/";
BuildingService.getInfoByid = function(id) {
     return $.getJSON(BuildingService.DETAILPREFIX+id+"?callback=?",
        function(data) {
            data.picsrc = BuildingService.PICPREFIX + id + BuildingService.PICPOSTFIX;
            data.description += "<img src='"+data.picsrc+"'width='100px' height='80px'";
            return data;
        }).error(function(){
            return null;
        });
};

BuildingService.setPopoverDetail = function(id) {
    $.getJSON(BuildingService.DETAILPREFIX + id+"?callback=?",
        function(data) {
            console.log(data.Name);
            console.log("==setPopoverDetail for "+data.id);
            console.log('#'+data.id);

            data.picsrc = BuildingService.PICPREFIX + id + BuildingService.PICPOSTFIX;
            console.log(data.picsrc);

            data.description += "<br><img src='"+data.picsrc+"' width='100px' height='80px'>";
            console.log(data.description);
            $('#'+data.id).popover({
                html: true,
                placement: 'top',
                trigger: 'click',
                title: data.name,
                content: data.description,
                container: 'body'
            });
        });
};
