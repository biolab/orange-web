/* ======= Trie search event handler ======= */
jQuery(document).ready(function ($) {
    var searchBox = $( "#search-box" );

    // on widget search box focus, scroll to it
    searchBox.focus(function () {
        $(document).scrollTop( $(this).offset().top - $( "header" ).height() - 70 );
    });

    // monitor text input
    searchBox.keyup(function () {
        // trigger input text retrieval
        var textval = $( this ).context.value;
        // get all widget h2s and lis
        var lis = $( "li.toctree-l1" );
        var h2s = $( "h2.widget-topic" );

        // hide if no input
        if (textval.length == 0) {
            lis.show(0);
            h2s.show(0);
            return;
        }

        // make search
        var results = window.trie.get(textval);

        // convert results to dictionary
        var resDict = {};
        results.forEach(function(el) {
            resDict[el.value] = el
        });

        // get widgets found by search
        var immRes;
        lis.each(function (idx) {
            immRes = resDict[idx];
            if (immRes === undefined) {
                $( this ).hide(0);
            }
            else {
                $( this ).show(0);
            }
        });

        // hide h2 titles that don't have any more li children
        h2s.each(function () {
            if ($( this ).next().find( "li:visible" ).length == 0) {
                $( this ).hide(0)
            }
            else {
                $( this ).show(0)
            }
        });
    });
});
