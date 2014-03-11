$(document).ready(function() {
	if (navigator.userAgent.match(/Android/i)) {
		$( ".barcode-button" ).hide();
		$( ".loading" ).show();
		
		window.setTimeout(function() {
		location.href = document.getElementsByClassName("barcode-button")[0].getElementsByTagName("a")[0].href;
		}, 500);
	}

  function iOSscan(url) {
    setTimeout(function() {
      // if pic2shop not installed yet, go to App Store
      window.location = "http://itunes.com/apps/pic2shop";
    }, 25);
    // launch pic2shop and tell it to open Google Products with scan result
    window.location=url;
  }

});