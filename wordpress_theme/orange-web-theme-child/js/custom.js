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

    /* nav-bar handling so it is aligned with the sidebar */
    function setSidebar() {
        var $mainNav = $('nav.main-nav');
        $mainNav.removeAttr('style');
        if ($(window).width() > 767) {
            var $widgetArea = $('div.widget-area');
            var widgetAreaPos = $widgetArea.offset();
            var widgetAreaRight = $(window).width() - widgetAreaPos.left - $widgetArea.width() - 50;
            $mainNav.css({'right': widgetAreaRight});
        }
    }
    setSidebar();

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

    function resizeHandler() {
        setSidebar();
        resizeImages();
    }
    $(window).resize(resizeHandler);
});
