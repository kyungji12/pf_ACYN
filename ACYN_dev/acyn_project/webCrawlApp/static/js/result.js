$(document).ready(function(){
    $('div.nav-tab').click(function(){
        console.log(this+"클릭");
        
        var tab_id = $(this).attr('data-tab');

        $('div.nav-tab').removeClass('current');
        $('div.platform').removeClass('current');

        $(this).addClass('current');
        $("#"+tab_id).addClass('current');
    });
});
