/*
 * jQuery JavaScript Extention - Issue Tracker
 * http://jquery.com/
 *
 * Author:      NSC, modified RSC for new layout (without <pre> tag)
 *              also move css to stylesheet
 * Date:        2015-09-01
 */
$(document).ready(function() {
    $("table.messages td.content").each(function() {
         if($(this).html().indexOf("-----Original Message-----") > -1) {
            $(this).find("div").wrapInner("<div class='pre'></div>");
            $(this).find("div.pre").unwrap();
            var oContent = $(this).find(".pre").html();
            var pos = oContent.indexOf("-----Original Message-----");
            var nContent = oContent.substr(0,(pos-1));
            var nAttachment = oContent.substr(pos,oContent.length);
            $(this).find(".pre").html(nContent).wrapInner("<div class='prewrap'></div>");
            var trigger = $("<a href='javascript:void(0)'><span>▶</span> attached mail</a>").appendTo($(this).find(".pre"));
            $(trigger).addClass('toggle')
            var mail = $("<div>"+nAttachment+"</div>").appendTo($(this).find("div.pre"));
            $(mail).addClass('attachment').hide();
            $(trigger).click(function() {
                $(this).parent("div").find(".attachment").slideToggle();
                    if($(this).find("span").html() == "▼") {$(this).find("span").html("▶");} else {$(this).find("span").html("▼");}
            });
            $(this).find("div.pre").addClass('prewrap').delClass('pre')
         }
    });
});
