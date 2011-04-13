$(document).ready(function() {

	// --------------
	// Timepicker
	// --------------

	$.datepicker.regional['de'] = {
		closeText: 'schließen',
		prevText: '&#x3c;zurück',
		nextText: 'Vor&#x3e;',
		currentText: 'heute',
		monthNames: ['Januar','Februar','März','April','Mai','Juni',
		'Juli','August','September','Oktober','November','Dezember'],
		monthNamesShort: ['Jan','Feb','Mär','Apr','Mai','Jun',
		'Jul','Aug','Sep','Okt','Nov','Dez'],
		dayNames: ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'],
		dayNamesShort: ['So','Mo','Di','Mi','Do','Fr','Sa'],
		dayNamesMin: ['So','Mo','Di','Mi','Do','Fr','Sa'],
		weekHeader: 'Wo',
		dateFormat: 'yy-mm-dd',
		firstDay: 1,
		isRTL: false,
		showMonthAfterYear: false,
		yearSuffix: '',
                };

	$.datepicker.regional['en'] = {
                dateFormat: 'yy-mm-dd',
                };


	$.timepicker.regional['de'] = {
		timeText: 'Zeit',
		hourText: 'Stunde',
		minuteText: 'Minute',
		currentText: 'Jetzt',
		closeText: 'Übernehmen',
                timeFormat: 'hh:mm:ss',
                separator: '.',
                };

	$.timepicker.regional['en'] = {
                timeFormat: 'hh:mm:ss',
                separator: '.',
                };

        l = $(".navi_lang").attr('lang')
	$.datepicker.setDefaults($.datepicker.regional[l]);
	$.timepicker.setDefaults($.timepicker.regional[l]);

	$( "#date_from" ).datetimepicker({
		showOn: "button",
		buttonImage: "@@file/lfiles/images/datepicker.png",
		buttonImageOnly: true
	});

	$( "#date_to" ).datetimepicker({
		showOn: "button",
		buttonImage: "@@file/lfiles/images/datepicker.png",
		buttonImageOnly: true
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

	$('#list_content .col_id, #list_content .col_name, #list_content .col_device, #list_content .col_group, #list_content .col_intervall, #list_content .col_desc, #list_content .col_order, #list_content .col_tz').each(function() {
		$(this).click(function() {
			
                        var listrow = $(this).parent('.list_row');
                        var detail = '#details_' + listrow.parent().attr('id');
                        $('.active_row').removeClass('active_row');
                        $('.active_detail').removeClass('active_detail');
                        listrow.addClass('active_row');
                        $(detail).addClass('active_detail');
		});
	});

        $('.list_header_link').click(function() {
            $('.active_row').removeClass('active_row');
            $('.active_detail').removeClass('active_detail');
            $('#details_new').addClass('active_detail');
        });

	// --------------
	// Funktionen zur Checkboxauswahl
	// --------------

	// Alle aktivieren
	$('.selectbox').attr('checked', true);

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
        // Dynamische Button-Borders
        // --------------
        
        jQuery('.buttonbox input').before('<span class="button_border_left"></span>').after('<span class="button_border_right"></span>')

	// --------------
	// Search form
	// --------------

	$("#queryname").focus(function(){
            if ($(this).attr('value') == $(this).attr('title'))
            {
                $(this).val ('');
            }
	});

	$("#queryname").change(function(){
            $("#old_queryname").val($(this).val());
	});

	$("#filterladen").change(function(){
            var v = $(this).attr('value');
            var n = $(this).children('option[value="'+v+'"]').text();
            $("#old_queryname").val(n);
            $("#queryname").val(n);
	});

	$("#form_csv").submit(function(){
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
                $('#rup_action').val('search');
            }
        });

        $("#load_filter").click(function(ev){
            var q = $("#filterladen");
            var v = q.attr('value');
            if (!v && ev && ev.preventDefault) {
                ev.preventDefault();
            } else {
                $('#rup_action').val('query_goto');
                $('#form_csv').attr('action', v);
            }
        });

        $("#device_select").change(function(){
            var v = $("#device_select").val();
            $("#device_input").val(v);
            $("#device_id").val(v);
        });

        $("#device_group_select").change(function(){
            var v = $("#device_group_select").val();
            $("#device_group_input").val(v)
            $("#device_group").val(v);
        });

        function copy_date(){
            var d = $('#measurementdate').attr('value');
            var ds = d.split(';');
            if (ds.length >= 1) {
                $("#date_from").val(ds[0]);
            }
            if (ds.length >= 2) {
                $("#date_to").val(ds[1]);
            }
            if (ds.length == 1) {
                $("#date_to").val(ds[0]);
            }
        }
        $("#measurementdate").ready(copy_date);
        $("#form_filter").bind('reset',function(){
            // ugly hack to call this after form has cleared
            setTimeout(copy_date, 1);
        });

        // reset password to remove 'helpful' browser behaviour 
        $(".settings_field").children('[type="password"]').attr('value','');
        $(".value").children('[type="password"]').attr('value','');

});
