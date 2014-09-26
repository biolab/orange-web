$.fn.visage.defaults.files = $.extend(true, {}, $.fn.visage.defaults.files, {
	"blank": "plugins/jquery-visage/res-alt/images/blank.gif",
	"error": "plugins/jquery-visage/res-alt/images/error.png"
});
$.fn.visage.defaults.attr = $.extend(true, {}, $.fn.visage.defaults.attr, {
	"close": {"id": "visage-alt-close"},
	"title": {"id": "visage-alt-title"},
	"count": {"id": "visage-alt-count"},
	"container": {"id": "visage-alt-container"},
	"image": {"id": "visage-alt-image", "src": "plugins/jquery-visage/res-alt/images/blank.gif"},
	"visage": {"id": "visage-alt"},
	"overlay": {"id": "visage-alt-overlay"},
	"prev": {"id": "visage-alt-nav-prev"},
	"prev_disabled": {"id": "visage-alt-nav-prev"},
	"next": {"id": "visage-alt-nav-next"},
	"next_disabled": {"id": "visage-alt-nav-next"}
});
$.fn.visage.defaults.enabledClass = "visage-alt-enabled";
$.fn.visage.defaults.disabledNavClass = "visage-alt-nav-disabled";
$.fn.visage.defaults.addDOM = function (visageDOM, options) {
	$.fn.visage.addDOM(visageDOM, options);
	// Moves elements to overlay so they are all in the same stacking context
	$(visageDOM.prev).add(visageDOM.next).add(visageDOM.count).add(visageDOM.title).appendTo(visageDOM.overlay);
};
$(document).ready(function () {
	var exts = /(\.jpg|\.jpeg|\.png|\.gif)$/i;

    $("#visage.imgcontent").each(function (i, el) {
		$("a[href]:has(img)", el).visage();
		$("a[href].enable-visage", el).visage({
			"imageValues": function (image, options) {
				var values = $.fn.visage.imageValues(image, options);
				// Image is not really a image here, but a link to an image with some text
				// content which we take as a title
				values.title = image.text();
				return values;
			}
		});
	});
});
