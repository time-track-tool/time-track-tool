$(document).ready(function() {
    $('.main div').click (function () {
        $(this).parent().parents('form').toggleClass('unmapped');
    });
});
