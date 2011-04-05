$(document).ready(function() {

	// --------------
	// Timepicker
	// --------------
	
	var timepickerOptions = { 
		format: '%d.%m.%z  %H:00',
		labelTitle: 'Datum und Zeit ausw&auml;hlen',
		labelHour: 'Uhrzeit',
		labelDayOfMonth: 'Tag',
		labelMonth: 'Monat',
		labelYear: 'Jahr',
		firstDOW: 1,
		dayAbbreviations: ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'],
		monthAbbreviations: ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
	}
	
  	$('img#datepick_from').click( function() {
    	$('#date_from').AnyTime_picker(timepickerOptions).focus();
    	$(this).unbind("click"); 
	});
	
  	$('img#datepick_to').click( function() {
    	$('#date_to').AnyTime_picker(timepickerOptions).focus();
    	$(this).unbind("click"); 
	});

	
	// --------------
	// Alles ein- und ausklappen
	// --------------
	
  $('img#main_collapse').each(function() {
	$(this).click(function() {
		if ($(this).hasClass('closed')) {
			$('#list_content img').removeClass('closed');
			$('ul.sensor').show('300');			
		} else {
			$('#list_content img').addClass('closed');		
			$('ul.sensor').hide('300');
		}
		$(this).toggleClass('closed');
	});
  });
	
	// --------------
	// Sensoren ein- und ausklappen
	// --------------
	
  $('#list_content img').each(function(){
		$(this).click( function() {
			$(this).toggleClass('closed');
			$(this).parents('li').find('ul.sensor').toggle('300');
			
			all_open = true;
			all_closed = true;
			$(this).parents('#list_content').find('img').each(function() {
				if($(this).hasClass('closed')) {
					all_closed = false;
				} else {
					all_open = false;
				}
			});		
			if(all_closed) $('#main_collapse').removeClass('closed'); 
			if(all_open) $('#main_collapse').addClass('closed'); 			
		});
	});

	
	// --------------
	// Element bei Klick auf Name hervorheben
	// --------------

	$('#list_content .col_id, #list_content .col_name, #list_content .col_device, #list_content .col_group, #list_content .col_intervall').each(function() {
		$(this).click(function() {
			
                        var listrow = $(this).parent('.list_row');
                        var detail = '#details_' + listrow.parent().attr('id');
                        $('.active_row').removeClass('active_row');
                        $('.active_detail').removeClass('active_detail');
                        listrow.addClass('active_row');
                        $(detail).addClass('active_detail');
		});
	});

	// --------------
	// Funktionen zur Checkboxauswahl
	// --------------

	// Alle aktivieren
	$('input[type=checkbox]').attr('checked', true);

	// Alle umschalten
	$("#list_header input").click(function(){
		var checked_status = this.checked;
		$('#list_content input').each(function(){
			this.checked = checked_status;
		});
	});	

	// Device-Checkboxen umschalten
	$(".list_row.main input").click(function(){
		var checked_status = this.checked;
		$(this).parents('li').find('.sensor input').each(function(){
			this.checked = checked_status;
		});
	});	

	// Sensor-Checkbox-Verhalten
	$('.sensor input').click(function() {
		if(!this.checked) $(this).parents('li.device').find('input[name=checker_main]').attr('checked', false);
		
		all_subs_checked = true;
		$(this).parents('li.device').find('input[name=checker_sub]').each(function() {
			if(!this.checked) all_subs_checked = false;
		});		
		if(all_subs_checked) $(this).parents('li.device').find('input[name=checker_main]').attr('checked', true); 
	});
		

	// --------------
	// Sortierung
	// --------------

	$('#list_header a').each(function() {

		$(this).addClass('asc');

		$(this).click(function(){
			var sort_class = '.' + $(this).parent().attr('class');
			if($(this).hasClass('active')) {
				if($(this).hasClass('asc')) {
					$(this).removeClass('asc').addClass('desc');
				} else {
					$(this).removeClass('desc').addClass('asc');				
				}
			} else {
				$('#list_header .active').removeClass('active');
				$(this).addClass('active');		
			}

			sort_order = {order: 'asc'};
			if($(this).hasClass('desc')) sort_order = {order: 'desc'};
			$('#list_content>li').tsort(sort_class, sort_order);
		});
	});

	// --------------
	// Search form
	// --------------

	$("#queryname").focus(function(){
            if ($(this).attr('value') == $(this).attr('title'))
            {
                $(this).val ('');
            }
	});

	$("#form_filter").submit(function(){
            var q = $("#queryname")
            var d = $('#measurementdate')
            if (q.attr('value') == q.attr('title'))
            {
                q.val ('');
            }
            d.val($('#date_from').val()+';'+$('#date_to').val())
            return true;
	});

        $("#save_filter").click(function(ev){
            var q = $("#queryname");
            var v = q.attr('value');
            if ((!v || v == q.attr('title')) && ev && ev.preventDefault) {
                ev.preventDefault();
            } else {
                $('#\\:action').val('search');
            }
        });
});
