var windowHasFocus;

$(window).focus(function() {
  windowHasFocus = true;
}).blur(function() {
  windowHasFocus = false;
});

function goScan(url, platform) {
  document.location = url;
  setTimeout(function(){
    if(windowHasFocus) {
      window.alert("I am an alert box!");
    }
  }, 100);
}

$('a.scanner_activate').on('click', function(){
  goScan($(this).data('url'), $(this).data('platform'));
});