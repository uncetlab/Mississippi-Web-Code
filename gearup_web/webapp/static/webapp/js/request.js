$(document).ready(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            document.cookie = createCookie('username', '{{ username }}', 1 );
            document.cookie = createCookie('password', '{{ password }}', 1 );
            document.cookie = createCookie('api_url', '{{ api_url }}', 1 );
        }
    });

    $.ajax({
        url: getCookie('api_url'),              
        type: "POST",          
        data: {
            username: getCookie('username'),
            password: getCookie('password'),
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function(data) {
            localStorage.token = data.access;
            sessionStorage.token = data.access;
            console.log("inside set_header");
            set_header(data.access);
        },
        error: function(e) {
            console.log(e);
            console.log("Login Failed");
        }
    });

    function set_header(token) {
        console.log("set_header");
        console.log(token);
//        $.ajaxSetup({
//            headers: {'Authorization', 'Bearer ' + token },
//        });
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function createCookie(name, value, hours){
        if (hours){
            var date = new Date();
            date.setTime(date.getTime()+(hours*60*60*1000));
            var expires = "; expires="+date.toGMTString();
        }
        else{
            var expires = "";
        }
        document.cookie = name+"="+value+expires+"; path=/";
    };
});