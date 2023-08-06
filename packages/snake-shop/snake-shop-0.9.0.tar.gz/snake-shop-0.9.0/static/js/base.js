
function urlAddParameter(url, param_string){
	var url = new URL(window.location);
	var search_params = url.searchParams;
	var search_params_to_add = new URLSearchParams(param_string);
	search_params_to_add.forEach(function(value, key){
		search_params.set(key, value)
	})
	return url.toString();
}

var currentProductPageRequest = null;
function loadProductPage(page){
	Waypoint.destroyAll();
	var url = new URL(window.location);
	url.searchParams.set('page', page);
	url.searchParams.set('format', 'ajax');
	if (page == 1) {
		var element = $('#products');
	} else {
		var element = $('#lazy_loading').parent();
	};
	var waypoint = new Waypoint({
		element: element,
		offset: '100%',
	  	handler: function(direction) {
		  currentProductPageRequest = $.ajax({
	  		url: url,
		  	context: document.body,
		    beforeSend : function()    {           
		        if(currentProductPageRequest != null) {
		            currentProductPageRequest.abort();
					console.log('aborted previous ajax');
		        }
		    },
		  	success: function(response){
				$('#lazy_loading').remove();
				$('#spinner').hide();
				$('#products').append(response);
	  			var old_num_results = $('#num_results').val();
				currentProductPageRequest = null;
		  	}
			});
		waypoint.destroy();
	  }
	})
	initializePopovers();
	initializeTooltips();
}


function refreshDynamicSiteData(){
    $.ajax({
        type: 'GET',
		dataType: 'json',
        url: dynamicDataUrl,
    }).done(function(response){
		$('#basket_items').html(response['basket_items']);
		$('#basket_value').html(response['basket_value']);
		$('#wishlist_items').html(response['wishlist_items']);
	})
}


function autoClose(){
	$('.autoclose').delay(3000).fadeOut();
}


function refreshMessages(){
    $.ajax({
        type: 'GET',
        url: messageAjaxUrl,
    }).done(function(response){
		$('#messages').append(response);
		autoClose();
	})
}


function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        // Internet Explorer-specific code path to prevent textarea being shown while dialog is visible.
        return window.clipboardData.setData("Text", text);

    }
    else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in Microsoft Edge.
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  // Security exception may be thrown by some browsers.
        }
        catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        }
        finally {
            document.body.removeChild(textarea);
        }
    }
}


/* Addtobasket */
function submitForm(form, url){
	var submit_button = form.find('button');
	submit_button.prop('disabled', true);
    var formData = {
        'csrfmiddlewaretoken'  : form.find('input[name=csrfmiddlewaretoken]').val(),
        'quantity'             : form.find('input[name=quantity]').val(),
		'ajax': true,
    };
    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
    }).done(function(response){
		$('#basket_items').html(response['basket_items']);
		$('#basket_value').html(response['basket_value']);
		submit_button.prop('disabled', false);
		submit_button.removeClass('text-dark')
		submit_button.addClass('text-success')
		refreshMessages();
	});
}


function submitAddWishlist(form, url){
	var submit_button = form.find('button');
    var formData = {
        'csrfmiddlewaretoken'  : form.find('input[name=csrfmiddlewaretoken]').val(),
    };
    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
    }).done(function(response){
		if (response['product_in_wishlist']){
			submit_button.html('<i class="fas fa-heart text-danger favourite"></i>');
		}else{
			submit_button.html('<i class="far fa-heart no-favourite"></i>');
		};
		$('#wishlist_items').html(response['wishlist_items']);
		refreshMessages();
	});
}


function submitReorder(form, url){
	/* var formData = new FormData(document.querySelector('form')) */
    var formData = {
        'csrfmiddlewaretoken'  : form.find('input[name=csrfmiddlewaretoken]').val(),
        'action'  : form.find('input[name=action]').val(),
    };
    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
    }).done(function(response){
		refreshDynamicSiteData();
		refreshMessages();
	});
}


function scrollanchor() {
	$('#scrollanchor').css('min-height', '80vh');
	document.querySelector('#scrollanchor').scrollIntoView();
}


function initializePopovers(){
	/* Simple Popover */
	if ($('[data-toggle="popover"]').length){
		$('[data-toggle="popover"]').popover({
		    html : true,
			container: 'body',
			sanitize: false,
		    content: function() {
		      	return $(this).siblings('.popover-content').html();
		    }
		})
	}

	/* Manual Popovers for Forms inside */
	if ($('[data-toggle="popover-manual"]').length){
		$('[data-toggle="popover-manual"]').popover({ 
		    html : true,
			container: 'body',
			sanitize: false,
			title : function(){
				return $(this).attr('data-title') + '<button onclick="$(this).closest(\'div.popover\').popover(\'hide\');" type="button" class="close" aria-hidden="true">&times;</button>';
			},
		    content: function() {
		      	return $(this).siblings('.popover-content').html();
		    }
		});
	}
}
function initializeTooltips(){
	if ($('[data-toggle="tooltip"]').length){
		$('[data-toggle="tooltip"]').tooltip();
	}
}


function searchPreview(){
	/* Dynamic loading of search preview - not used now */
    var form = $(this);
	var url = new URL(window.location);
	var search_params = url.searchParams;
	url.pathname = searchPreviewUrl

	var new_q_value = $('#search_form_input').val();
	if(new_q_value){
		search_params.set('q', new_q_value);
	}else{
		search_params.delete('q');
	}
	search_params.set('format', 'ajax');
	
    $.ajax({
		type: "GET",
		url: url,
		data: form.serialize(), // serializes the form's elements.
		success: function(data){
			$('#search_results').html(data);
			//window.history.replaceState( {} , null, new_url_location );
		}
	});
}


function submitOrderForm(form){
	var url = new URL(window.location);
	var urlSearchParams = url.searchParams;
	var formData = new FormData(form);
	urlSearchParams.set('sort_by',formData.get('sort_by'));
	window.history.pushState({}, '', url);
	$('#products li').remove();
	Waypoint.destroyAll();
	$('#spinner').show();
	loadProductPage(1);
}


function submitFilterForm(form){
	event.preventDefault();
	$('#products li').remove();
	Waypoint.destroyAll();
	$('#spinner').show();
	/* Extract url and search params */
	var url = new URL(window.location);
	var urlSearchParams = url.searchParams;
	var searchParams = new URLSearchParams(url.search);
	searchParams.forEach(function(value, key){
		if (key != 'q' && key != 'sort_by'){
			urlSearchParams.delete(key);
		}
	});
	var formData = new FormData(form);
	var search_params = new URLSearchParams(formData);
	search_params.forEach(function(value, key){
		if (value.length > 0){
			urlSearchParams.append(key, value);
		}
	})
	window.history.pushState({}, '', url);
	reloadSidebarForm(url);
	//initializeSidebarForm();
	loadProductPage(1);
}


function resetFilterForm(form){
	event.preventDefault();
	$('#products li').remove();
	Waypoint.destroyAll();
	$('#spinner').show();
	var url = new URL(window.location);
	var urlSearchParams = url.searchParams;
	var searchParams = new URLSearchParams(url.search);
	searchParams.forEach(function(value, key){
		if (key != 'q' && key != 'sort_by'){
			urlSearchParams.delete(key);
		}
	})
	window.history.pushState({}, '', url);
	reloadSidebarForm(url);
	//initializeSidebarForm();
	loadProductPage(1);
}


function reloadSidebarForm(url){
	$('.filter_form input').prop('disabled', true);
	$('.chosen-search-input').prop('disabled', true);
	var sidebar_url = new URL(url);
	var urlSearchParams = sidebar_url.searchParams;
	urlSearchParams.set('format', 'sidebar')
    $.ajax({
        type: 'GET',
        url: sidebar_url,
    }).done(function(response){
		$('.filter_form_ajax_block').html(response);
		initializeSidebarForm();
	})
}


function initializeSidebarForm(){
	if ($(".chosen-select").length){
		$(".chosen-select").chosen({
			placeholder_text_single: "Suche Option...",
			placeholder_text_multiple: "Suche Option...",
		});
		$(".chosen-select").chosen().off().on('change', function (){
			submitFilterForm(this.form);
		});
		initializeSidebarToggler();
	}
}


function initializeSidebarToggler(){
	$('.sidebar-toggler').off().on('click', function () {
		$(this).find('.rotate').toggleClass('rotated');
		var url = new URL(toggleSidebarUrl, base_url);
		var searchParams = url.searchParams;
		searchParams.set('sidebar-block', $(this).data('block'));
	    $.ajax({
	        type: 'GET',
	        url: url,
	    }).done();
	});
}


function initializeScrollTopButton(){
	if ($('#scroll_top_button').length){
		$(window).scroll(function (event) {
		    var scroll = $(window).scrollTop();
		    if(scroll >= 1000){
			   $('#scroll_top_button').fadeIn();
			}else{
			   $('#scroll_top_button').fadeOut();
			};
		});
	}
}


function initializeCategoryMenus(){
	if ($("#main_categories").length){
		var slider1 = tns({
			"container": "#main_categories",
			"gutter": 15,
			"autoWidth": true,
			"slideBy": 1,
			"autoplay": false,
			"mouseDrag": true,
			"swipeAngle": false,
			"autoplayTimeout": 3000,
			"speed": 400,
			"arrowKeys": true,
			"autoplayHoverPause": true,
			"controls": false,
			"autoplayButton": false,
			"autoplayButtonOutput": false,
			"nav": false,
			"loop": false,
		});
		$('#main_categories').css('display', '');
	}
	if ($("#sub_categories").length){
		var slider2 = tns({
			"container": "#sub_categories",
			"gutter": 15,
			"autoWidth": true,
			"slideBy": 1,
			"autoplay": false,
			"mouseDrag": true,
			"swipeAngle": false,
			"autoplayTimeout": 3000,
			"speed": 400,
			"arrowKeys": true,
			"autoplayHoverPause": true,
			"controls": false,
			"autoplayButton": false,
			"autoplayButtonOutput": false,
			"nav": false,
			"loop": false,
		});
		$('#sub_categories').css('display', '');
	}
}

function fontFitHeight(element){
	var elementHeight = $(element).outerHeight();
	var lines = $(element).data('font-fit-lines');
	if (lines != undefined){
		elementHeight = elementHeight / lines
	}
	$(element).css('font-size', elementHeight);
}

function fontFitExecuter(){
	$('.font-fit-height').each(function(){
		fontFitHeight(this);
		$(this).removeClass('invisible');
	})
}

function fontFitExecuterTrigger(){
	if ($('.font-fit-height').length){
		$(window).resize(function (){
			setTimeout(function() {
			    fontFitExecuter();
			}, 500);
	    });
		$('.resize-trigger').one('load',function() {
			setTimeout(function() {
	    	    fontFitExecuter();
			}, 500);
	    });
		setTimeout(function() {
	        fontFitExecuter();
	    }, 500);
		setTimeout(function() {
	        fontFitExecuter();
	    }, 1000);
		setTimeout(function() {
	        fontFitExecuter();
	    }, 2000);
		setTimeout(function() {
	        fontFitExecuter();
	    }, 3000);
	};
}


$(function() {
	fontFitExecuterTrigger();
	initializeCategoryMenus()
	initializeSidebarForm();
	initializePopovers();
	initializeTooltips();
	initializeScrollTopButton();
});
