

// // just 4 secand showing message
// setTimeout(function(){
//     $('#message').fadeOut('slow');
// }, 4000);

document.querySelectorAll('input[dir="ltr"]').forEach(function(input) {
    if (document.documentElement.lang === 'ar') {
        input.style.unicodeBidi = 'bidi-override';
        input.style.direction = 'rtl';
    }
});
