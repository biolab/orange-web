/* ======= Custom js ======= */
jQuery(document).ready(function ($) {
    'use strict';

    // Allow tooltips only when using non-mobile devices
    if (jQuery.browser.mobile === false) {
        $('.alert').alert();
    }

    function loadFBGP() {
        /* Facebook */
        if (window.location.pathname.length > 1) {
            return;
        }
        (function (d, s, id) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) {
                return;
            }
            js = d.createElement(s);
            js.id = id;
            js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.0";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));

        /* Google +1 */
        window.___gcfg = {
          lang: 'en-US',
          parsetags: 'onload'
        };
        (function() {
            var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
            po.src = 'https://apis.google.com/js/plusone.js?onload=onLoadCallback';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
        })();
    }
    loadFBGP();

    function resizeImages() {
        var pImgs = $('.features .content p img');
        pImgs.removeAttr('style');
        var pWidth = $('.features .content p').width();
        pImgs.each(function(i, el) {
            if ( pWidth < $(this, el).width() ) {
                $(this, el).css('width', pWidth);
            }
        });
    }
    resizeImages();

    $(window).resize(resizeImages);
});

jQuery(document).ready(function() {
    $('.pop').on('click', function() {
        var img_src = $(this).find('img').attr('src').replace("thumbs/", "");
        var carousel_element = document.getElementsByClassName("carousel-inner")[0];
        var carousel_images = carousel_element.getElementsByTagName("img");
        for (i = 0; i < carousel_images.length; i++) {
            var image = carousel_images[i]
            $(image).parent().removeClass('active');
            if (image.getAttribute("src") == img_src) {
                $(image).parent().addClass('active');
            }
        }
        $('#imagemodal').modal('show');
    });
    $('.carousel').carousel({
      interval: 0
    });
});


