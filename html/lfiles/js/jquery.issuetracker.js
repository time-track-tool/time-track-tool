/*
 * jQuery JavaScript Extention - Issue Tracker
 * http://jquery.com/
 *
 * Author: 	NSC
 * Date:	2015-09-01
 * Verison:	0.2s 
 */
$(document).ready(function() {
    $("table.messages td.content").each(function() {
     	 if($(this).html().indexOf("-----Original Message-----") > -1) {
            $(this).find("pre").wrapInner("<div class='pre'></div>"); 
            $(this).find("div").unwrap(); 
            var oContent = $(this).find(".pre").html();
            var pos = oContent.indexOf("-----Original Message-----");             
            var nContent = oContent.substr(0,(pos-1));    
            var nAttachment = oContent.substr(pos,oContent.length);   
            $(this).find(".pre").html(nContent).wrapInner("<pre></pre>");
            var trigger = $("<a href='javascript:void(0)'><span>▶</span> attached mail</a>").appendTo($(this).find(".pre"));
            $(trigger).css({'text-decoration':'none','border':'1px solid #CCC','border-radius':'2px','padding':'3px'});             
            var mail = $("<div>"+nAttachment+"</div>").appendTo($(this).find("div"));           
            $(mail).addClass('attachment').hide().css({'margin-left':'20px','border-left':'1px solid #CCC','padding-left':'5px'});             
            $(mail).wrapInner("<pre></pre>");
            $(trigger).click(function() {
            	$(this).parent("div").find(".attachment").slideToggle();
                    if($(this).find("span").html() == "▼") {$(this).find("span").html("▶");} else {$(this).find("span").html("▼");}  
            });              
         }
    });
});