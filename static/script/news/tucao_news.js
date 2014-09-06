$(document).ready(function() {
	$('.reply-btn').attr('href','#input-addon');

	$('.reply-btn').click(function() {
		$('#input-addon').text('To '+$(this).attr('id')+'F');
		$('#dest-floor-id').attr('value', $(this).attr('id'));
	});

	$('#tucao-btn').click(function() {
        $.post("/news",{
            id:$('#id').attr('value'),
            content: $('textarea[name="tucao-content"]').val(),
            level: $('#dest-floor-id').attr('value'),
            _xsrf: $("input[name='_xsrf']").val()
        },
        function() {
            //console.log(res);
            window.location.reload();
        });
    });

	var pageid = parseInt($('#id').attr("value"));
    var latest = parseInt($('#latest').attr("value"));
    var total = parseInt($('#total').attr("value"));
    var oldest = latest - total + 1;
	
    var prevpage = pageid - 1;
    var nextpage = pageid + 1; 
	
    
    if ( pageid != oldest )
    {
        $('.previous').find('a').attr('href', "/news/"+prevpage);
    } else {
        $('.previous').addClass('disabled');
    }

    if ( pageid != latest )
    {
		$('.next').find('a').attr('href', "/news/"+nextpage);
	} else {
        $('.next').addClass('disabled');
    }
});
