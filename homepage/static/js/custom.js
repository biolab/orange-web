/* ======= Custom js ======= */
jQuery(document).ready(function ($) {
    'use strict';

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

    function setYouTubeDimensions () {
        var width = $( window ).width();
        var height = $( window ).height();

        // constants
        var maxWidth = 720;
        var maxHeight = 405;

        // new
        var newMaxWidth = width * 0.9;
        var newMaxHeight = height * 0.9;

        if (newMaxHeight < maxHeight * 0.9) {
            height = Math.round(newMaxHeight);
            width = Math.round(height * 1.7778);
        }
        else if (newMaxWidth < maxWidth * 0.9) {
            width = Math.round(newMaxWidth);
            height = Math.round(width * 0.5625);
        }
        else {
            width = maxWidth;
            height = maxHeight;
        }
    }

    function disableDownloadButton() {
        $( "#main-page-download-button" ).parent().hide(0);
    }

    // Allow colorbox and dynamic image resizing only when using
    // non-mobile devices
    if (!jQuery.browser.mobile) {
        setYouTubeDimensions();

        $(window).on('resize', function () {
            setYouTubeDimensions();
        });
    }
    else {
        disableDownloadButton();
    }
});
