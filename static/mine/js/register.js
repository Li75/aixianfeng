$(function () {
    $('.register').width(innerWidth)


    $('#username input').blur(function () {
        if ($(this).val() == '') return
        if ( $(this).val().length>=3 || $(this).val().length<=10 ){  // 可用
            $('#username').removeClass('has-error').addClass('has-success')
            $('#username>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        } else {    //不可用
            $('#username').removeClass('has-success').addClass('has-error')
            $('#username').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })


    $('#password input').blur(function () {
        var reg = new RegExp("^[a-zA-Z0-9_]{6,10}$");
        if ($(this).val() == '') return
        if ( reg.test( $(this).val() ) ){  // 可用
            $('#password').removeClass('has-error').addClass('has-success')
            $('#password>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        } else {    // 不可用
            $('#password').removeClass('has-success').addClass('has-error')
            $('#password>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })


    $('#phone input').blur(function () {
    var reg = /^1(3|4|5|7|8)\d{9}$/;
    if ($(this).val() == '') return
    if ( reg.test( $(this).val() ) ){  // 可用
        $('#phone').removeClass('has-error').addClass('has-success')
        $('#phone>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
    } else {    // 不可用
        $('#phone').removeClass('has-success').addClass('has-error')
        $('#phone>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
    }
})



    $('#subButton').click(function () {
        console.log('注册')
        var isregister = true

        $('.register .form-group').each(function () {
            if( !$(this).is('.has-success') ) {
                isregister = false
            }
        })
        if (isregister){
            $('.register form').submit()
        }
    })
})
