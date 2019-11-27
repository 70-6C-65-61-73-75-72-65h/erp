$("#change_passives").click(function(){
    if ($("#passives").is(":hidden")){
        $("#passives").css('display', 'block');
    }
    else{
        $("#passives").css('display', 'None');
    }
});

$("#change_assets").click(function(){
    if ($("#assets").is(":hidden")){
        $("#assets").css('display', 'block');
    }
    else{
        $("#assets").css('display', 'None');
    }
});