$(document).ready(function() {

	if (navigator.userAgent.match(/Android/i)) {
		$( ".barcode-button" ).hide();
		$( ".barcode-button a" ).click();
	}

});