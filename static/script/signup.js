var validity_checking_url="/api?callback=?";
var post_url = "/signup";
//validity_checking_url = "test.js";
var email_key=0;
var name_key=0;
var password_key=0;
var password_confirmation_key = 0;

$(document).ready(function() {
	$('#email-address').bind('input propertychange blur', validity_checking);
	$('#nick-name').bind('input propertychange blur', validity_checking);
	$('#password').bind('input propertychange blur', is_password_legal);
	$('#password-confirmation').bind('input propertychange blur', is_password_matched);
	//$('#submit').click(submit_register_form);
	//init();
		is_password_legal();
		is_password_matched();
		
		$('#email-address').blur();
		$('#nick-name').blur();
});

	function init() {
		$('#email-address').val($.cookie('email'));
		$('#nick-name').val($.cookie('name'));
		$('#password').val($.cookie('password'));
		$('#password-confirmation').val($.cookie('repassword'));
	}

	function save_form_to_cookie(email, nickname, password1, password2, is_subscribed) {
		$.cookie('email', email);
		$.cookie('name', nickname);
		$.cookie('password', password1);
		$.cookie('repassword', password2);
        $.cookie('is_subscribed', is_subscribed);
	}
	function submit_register_form() {
		var email = $('#email-address').val();
		var nickname=$('#nick-name').val();
		var password1=$('#password').val();
		var password2=$('#password-confirmation').val();
		var is_subscribed=$('#is-subscribed').checked ? 1 : 0;

		is_password_legal();
		is_password_matched();
		
		$('#email-address').change();
		$('#nick-name').change();

		save_form_to_cookie(email,nickname,password1,password2, is_subscribed);

        if (email_key && name_key && password_key && password_confirmation_key) {
		    post_register_data(email, nickname, password1, password2, is_subscribed);
        }
	}

    function post_register_data(email, name, password, repassword, is_subscribed) {
            _xsrf = $.cookie('_xsrf');
            if (_xsrf == "") {
                _xsrf = "abc";
            }
             $.post(post_url, {
                    email: email,
                    name: name,
                    password: password,
                    repassword: repassword,
                    is_subscribed: is_subscribed,
                    _xsrf: _xsrf,
                });
    }

	function is_password_legal() {
		var passwd=$('#password').val();
		if (passwd.length < 8  || passwd.length > 16) {
			// 密码长度不正确
			$('#password').siblings(':first').html("密码长度不正确");
            password_key = 0;
			return -1;
		} else {
			$('#password').siblings(':first').html("推荐8-16位字母、数字组合");
            password_key = 1;
			return 0;
		}

        switch_submit_btn();
	}

	function is_password_matched() {
		var passwd1=$('#password').val();
		var passwd2=$('#password-confirmation').val();
		if (passwd1 != passwd2) {
			// 两次密码不匹配
			$('#password-confirmation').siblings(':first').html("两次密码不匹配");
            password_confirmation_key = 0;

            $('#submit').addClass('btn-disabled');
			return -1;
		} else {
			$('#password-confirmation').siblings(':first').html("");
            password_confirmation_key = 1;

            switch_submit_btn();
			return 0;
		}
	}


	function validity_checking(type, value) {
		type = $(this).attr('id')=="nick-name" ? "NAME" : "EMAIL";
		value = $(this).val();
		if (value == "") {
			// 不能为空
			$(this).siblings(':first').html("不能为空");
			return 0;
		}
		$.getJSON(validity_checking_url,{
			type: type,
			value: value, 
			}, function(data){
				var label_id = data.type=="EMAIL" ? "email-address":"nick-name";
				if (data.status == "UNIQUE") {
					$('#'+label_id).siblings(':first').html(data.type+"可以使用");
                    data.type=="EMAIL"?email_key=1:name_key=1;
				}
				//if (data.status == "REPEATED") {
                else {
					$('#'+label_id).siblings(':first').html(data.type+"不可使用");
                    data.type=="EMAIL"?email_key=0:name_key=0;
				}
			});
        switch_submit_btn();
	}

    function switch_submit_btn() {
        if (email_key && name_key && password_key && password_confirmation_key) {
            $('#submit').removeClass('disabled');
        } else {
            $('#submit').addClass('disabled');
        }
    }

