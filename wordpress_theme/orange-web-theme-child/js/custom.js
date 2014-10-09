/* ======= Blog js modifications ======= */

$(document).ready(function() {
    /* enable jquery-visage */
    function appendVisage() {
        var $imgs = $('div.entry-content:has(a[href]:has(img))');
        if ($imgs.length) {
            $imgs.each(function(i, el) {
                $(this, el).attr('id', 'visage').addClass('imgcontent');
            });
        }
    }
    appendVisage();

    function resizeImages() {
        var $pImgs = $('.entry-content p img').removeAttr('style');
        var pWidth = $('.entry-content p').width();
        $pImgs.each(function(i, el) {
            if ( pWidth < $(this, el).width() ) {
                $(this, el).css('width', pWidth);
            }
        });
    }
    resizeImages();
    $(window).resize(resizeImages);
});
