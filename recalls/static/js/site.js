$(document).ready(function() {
	var windowHasFocus = true;
	
	$(window).focus(function() {
		windowHasFocus = true;
	}).blur(function() {
		windowHasFocus = false;
	});
	
	function goScan(url) {
		document.location = url;
		setTimeout(function(){
			if(windowHasFocus) {
				$('#scan-app-modal').modal();
			}
		}, 100);
	}

	$(".scanner_activate").click(function() {
		goScan($(this).data('url'));
	});
  
	$(".install_app").click(function() {
    $('#myModal').modal('hide');
    window.location.href = $(this).data('url');
	});
});