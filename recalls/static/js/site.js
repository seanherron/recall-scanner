$(document).ready(function() {
	if (navigator.userAgent.match(/Android/i)) {
		$( ".barcode-button" ).hide();
		$( ".loading" ).show();
		
		window.setTimeout(function() {
		location.href = document.getElementsByClassName("barcode-button")[0].getElementsByTagName("a")[0].href;
		}, 500);
	}

});