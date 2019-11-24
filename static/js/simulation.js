function refresh_simulation(sim){
    var to_url = $(sim).attr('data-to-url'); 
    var from_url = $(sim).attr('data-from-url');
    var ajaxdata = {
        from_url: from_url,
    };
    $.ajax({
        url: to_url,
        data: JSON.stringify(ajaxdata),
        dataType: 'json',
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        },
        success: function(result){
            for (var key in result) {
                var sentence = '';
                sentence = key + ': ' + result[key]
                $("#" + key + "").text(sentence);
            };
        }
    });
};