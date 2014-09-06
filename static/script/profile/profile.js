$(document).ready(function() {
		$('#cgname').click(function() {
			$.post('/api/cgname', {
				new_name: $('input[name="username"]').val(),
                _xsrf: $("input[name='_xsrf']").val()
				},
				function() {
					console.info("success");
				}).error(function() {
					console.error("fail");
			    });
        });
		$('#cgpasswd').click(function() {
			$.post('/api/cgpasswd',{
					passwd: $('input[name="old-password"]').val(),
					new_passwd: $('input[name="new-password"]').val(),
					re_new_passwd: $('input[name="new-repassword"]').val(),
                    _xsrf: $("input[name='_xsrf']").val()
				},
				function() {
					console.info("success");
				}).error(function() {
					console.error("fail");
			    });
        });
});
