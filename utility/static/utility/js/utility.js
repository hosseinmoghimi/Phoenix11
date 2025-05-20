let TASVIEH = 'تسویه'
let BEDEHKAR = 'بدهکار'
let BESTANKAR = 'بستانکار'
let TUMAN = 'تومان'
let RIAL = 'ریال'
let SUCCEED = "SUCCEED"
let FAILED = "FAILED"
var to_price = function (x, currency) {
    if (x == null)
        return ""
    if (typeof currency === 'undefined')
        currency = ''
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' ' + currency
}



var showNotification = function (from, align, icon, bgcolor, html, rtl = true,farsi=false) {
    
    if (rtl) html = `<div class="text-right`+(farsi?' farsi ':'')+`">` + html + `</div>`

    type = ['', 'info', 'danger', 'success', 'warning', 'rose', 'primary'];

    color = Math.floor((Math.random() * 6) + 1);
    color = 3;
    $.notify({
        icon: icon,
        message: html

    }, {
        type: bgcolor,
        timer: 20000,
        placement: {
            from: from,
            align: align
        }
    });
}