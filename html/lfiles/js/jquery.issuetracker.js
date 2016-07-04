/*
 * jQuery JavaScript Extention - Issue Tracker
 * http://jquery.com/
 *
 * Author:      NSC
 * Revision:	2
 * Date:        2016-07-02
 */
$(document).ready(function() {
	String.prototype.regexIndexOf = function(regex, startpos = 0) {
		var indexOf = this.substring(startpos || 0).search(regex);
		return (indexOf >= 0) ? (indexOf + (startpos || 0)) : indexOf;
	}	
	var messageSplit = "(-----Original Message-----)|(---Original Nachricht---)"; //regex
	
    $("table.messages td.content").each(function() {
         if($(this).find("div.prewrap").html().regexIndexOf(messageSplit) > -1) {
			var pos 		= $(this).find("div.prewrap").html().regexIndexOf(messageSplit);
			var preTXT		= $(this).find("div.prewrap").html().substr(0,(pos-1));
			var messageTXT	= $(this).find("div.prewrap").html().substr(pos,$(this).find("div.prewrap").html().length);
			$(this).find("div.prewrap").html(preTXT);
            var trigger = $("<a href='javascript:void(0)' class='toggle'><span>▶</span> attached mail</a>").appendTo($(this).find("div.prewrap"));
			var mail = $("<br /><div>"+messageTXT+"</div>").appendTo($(this).find("div.prewrap"));
			$(mail).addClass('attachment').hide();	
            $(trigger).click(function() {
                $(this).parent("div").find(".attachment").slideToggle();
                    if($(this).find("span").html() == "▼") {$(this).find("span").html("▶");} else {$(this).find("span").html("▼");}
            });			
			pos = null;
			preTXT = null;
			messageTXT = null;
			trigger = null;
			mail = null;
         }
    });
});
