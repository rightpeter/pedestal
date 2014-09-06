$(document).ready(function() {

	var pageid = parseInt($('#id').attr("value"));
    var latest = parseInt($('#latest').attr("value"));
    var total = parseInt($('#total').attr("value"));
    var oldest = latest - total + 1;
	
    var prevpage = pageid - 1;
    var nextpage = pageid + 1; 
	// 隐藏两个按钮
//	$('#prevpage').hide();
//	$('#nextpage').hide();
	
	// url-prevpage url-nextpage 换成指定页面的url
    
    if ( pageid != oldest )
    {
        $('#prevpage').attr('href', "/news/"+prevpage);
        $('#prevpage').removeClass('disabled');
    }

    if ( pageid != latest )
    {
		$('#nextpage').attr('href', "/news/"+nextpage);
        $('#nextpage').removeClass('disabled');
	}

	$('#content').keyup(function() {
		$('#rest-num').text($('#content').val().length+"/240");
	});
	
	$('.level-reply a').click(function() {
		var level = $(this).parent().parent().attr('id');
		$('#content').text('@'+level+': ');
	});

	$('#tucao-submit').click(function() {
		//if($('#content').val().length > 240) {
			
		//}
            $.post("/news?"+(new Date()).valueOf(), {id: $('#id').attr("value"),content: $('#content').val(),_xsrf: $("input[name='_xsrf']").val()}, function (res) {
			console.log(res);
			window.location.reload();
		});
	});

    $(".body-full").hide();
    // 点击 more 显示更多内容
    $(".body-abstract").click(function() {
        $(".body-full").show("fast");
        $(".body-abstract").hide();
    });
});
