$(function() {
    $('.sidebar-toggle').click(function(e) {
        e.preventDefault();
        $('.left-side').toggleClass("collapse-left");
        $(".right-side").toggleClass("strech");
    });

    $('.delete').click(function(e) {
        e.preventDefault();
        if (confirm("确认删除?") == true) {
            var url = $(this).attr("href");
            var tr = $(this).closest("tr");
            $.getJSON(url, function (data) {
                if (data.state == 1) {
                    tr.remove();
                }
            })
        }
    });

    $('.pagination  a').click(function() {
       var url = $(this).attr('href');
       var page_size = $('#page-size').val();
       $(this).attr('href', url + page_size);
       return true;
    });

    $("#page-size").change(function(){
        var page_size = $(this).val();
        if(!(/^\+?\d+$/.test(page_size)) || page_size <= 0){
            alert("请输入正确的数字！");
            return false;
        }
        $("#page-form").submit();
    });

});