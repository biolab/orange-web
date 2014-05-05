/*
 * Mitar <mitar.jquery@tnode.com>
 * http://mitar.tnode.com/
 * BSD licensed.
*/

(function ($) {
	$.fn.visage = function (options) {
		if (!$.isReady) {
			warn("Use of Visage before DOM was ready");
			return this;
		}
		
		options = $.extend(true, {}, $.fn.visage.defaults, options);
		
		if (!options.isSupported(options)) {
			warn("Unsupported browser, will not use Visage");
			return this;
		}
		
		if (this.length == 0) {
			warn("Use of Visage on an empty group of elements");
			return this;
		}
		
		// Group of elements we are calling visage on
		var group = this;

		if (options.registerEvents) {
			group.unbind("click").click(function (event) {
				event.preventDefault();
				start(group.index(this), group, options);
				return false;
			});

			if (options.enabledClass) {
				group.addClass(options.enabledClass);
			}
		}
		
		if (options.start) {
			start(0, group, options);
		}

		return this;
	};
	
	$.fn.visage.isSupported = function (options) {
		// TODO Add workarounds if possible for unsupported browsers
		// A workaround for not supporting "position fixed" could be using "position absolute" and hiding/disabling scrollbars
		return $.support.positionFixed;
	};
	
	$.fn.visage.addDOM = function (visageDOM, options) {
		visageDOM.close = $("<div />").attr(options.attr.close).css(options.css.close);
		visageDOM.title = $("<div />").attr(options.attr.title).css(options.css.title);
		visageDOM.count = $("<div />").attr(options.attr.count).css(options.css.count);
		visageDOM.container = $("<div />").attr(options.attr.container).css(options.css.container);
		visageDOM.image = $("<img />").attr(options.attr.image).css(options.css.image);
		visageDOM.visage = $("<div />").attr(options.attr.visage).css(options.css.visage);
		visageDOM.overlay = $("<div />").attr(options.attr.overlay).css(options.css.overlay);
		visageDOM.prev = $("<div />").attr(options.attr.prev).css(options.css.prev);
		visageDOM.next = $("<div />").attr(options.attr.next).css(options.css.next);
		
		visageDOM.overlay.append(visageDOM.close);
		visageDOM.container.append(visageDOM.image);
		visageDOM.visage.append(visageDOM.container).append(visageDOM.prev).append(visageDOM.next).append(visageDOM.count).append(visageDOM.title);	
		
		$(visageDOM.visage).add(visageDOM.overlay).add(visageDOM.prev).add(visageDOM.next).hide();
		
		$("body").append(visageDOM.overlay).append(visageDOM.visage);
	};
	
	$.fn.visage.removeDOM = function (visageDOM, options) {
		$(visageDOM.overlay).add(visageDOM.visage).remove();
	};
	
	$.fn.visage.displayCount = function (current, all, visageDOM, options) {
		if (all > 1) {
			visageDOM.count.html("Image " + current + " of " + all);
		}
	};
	
	$.fn.visage.displayTitle = function (title, visageDOM, options) {
		visageDOM.title.html(title);
	};
	
	$.fn.visage.displayPrev = function (current, all, visageDOM, options) {
		if (current > 1) {
			visageDOM.prev.attr(options.attr.prev).css(options.css.prev).removeClass(options.disabledNavClass).show();
		}
		else if (all > 1) {
			visageDOM.prev.attr(options.attr.prev_disabled).css(options.css.prev_disabled).addClass(options.disabledNavClass).show();
		}
	};
	
	$.fn.visage.displayNext = function (current, all, visageDOM, options) {
		if (current < all) {
			visageDOM.next.attr(options.attr.next).css(options.css.next).removeClass(options.disabledNavClass).show();
		}
		else if (all > 1) {
			visageDOM.next.attr(options.attr.next_disabled).css(options.css.next_disabled).addClass(options.disabledNavClass).show();
		}
	};
	
	$.fn.visage.imageValues = function (image, options) {
		var values = {};
		
		values.src = image.attr("href") || image.attr("src") || "";
		
		if (values.src) {
			values.title = image.find("img[title]").attr("title") || image.find("img[alt]").attr("alt") || image.attr("title") || image.attr("alt") || "";
		}
		else {
			values.title = currentOptions.text.error;
			values.src = currentOptions.files.error;
		}
		
		return values;
	};
	
	$.fn.visage.showVisage = function (visageDOM, isStopping, finish, options) {
		visageDOM.overlay.css("opacity", options.opacity).fadeIn(options.onoffSpeed, function () {
			if (!isStopping()) {
				visageDOM.overlay.show();
				visageDOM.visage.show();
			}
			finish();
		});
	};
	
	$.fn.visage.hideVisage = function (visageDOM, finish, options) {
		visageDOM.visage.stop(true, true).hide();
		visageDOM.overlay.stop(true, true).fadeOut(options.onoffSpeed, function () {
			visageDOM.overlay.hide();
			visageDOM.visage.hide(); // To be sure
			finish();
		});
	};
	
	$.fn.visage.resizeVisage = function (css, transition, visageDOM, isStopping, finish, options) {
		visageDOM.visage.stop(true, true).animate(css, transition ? options.transitionResizeSpeed : options.windowResizeSpeed, function () {
			if (!isStopping()) {
				// Correct any bugs there might be
				// This makes image size absolute so it does not scale so nicely when window is resized but it is (probably) bullet-proof to look nice (and correct) at the end
				if (visageDOM.image.height() != visageDOM.container.height()) {
					visageDOM.image.height(visageDOM.container.height());
				}
				if (visageDOM.image.width() != visageDOM.container.width()) {
					visageDOM.image.width(visageDOM.container.width());
				}
			}
			
			finish();
		}).css({"overflow": "visible"}); // Has to set overflow to override default "hidden" value during jQuery animate
	};
	
	// A demonstration how to limit loadingTimeout scope just for internal use in those functions, which are an example
	// how to define images transition (and just a default)
	(function () {
		var loadingTimeout = null;
		
		$.fn.visage.beginStop = function (visageDOM, options) {
			// Clear any pending timeout
			if (loadingTimeout != null) {
				clearTimeout(loadingTimeout);
				loadingTimeout = null;
			}
		};
		
		// We should check ((group != null) && !isStopping()) in an animation finish callback if we are using it
		// (It has been checked before calling this function, but it is necessary to do it in asynchronous code)
		$.fn.visage.preImageLoad = function (values, group, visageDOM, isStopping, finish, options) {
			options.displayTitle(values.title, visageDOM, options);
			
			// Uses a short timeout so that display does not flicker if the image is already loaded
			if (options.loadingWait > 0) {
				loadingTimeout = setTimeout(function () {
					visageDOM.image.attr("src", options.files.blank);
				}, options.loadingWait);
			}
			else {
				visageDOM.image.attr("src", options.files.blank);
			}
			
			finish();
		};
		
		// We should check ((group != null) && (image != null) && !isStopping()) in an animation finish callback if we are using it
		// (It has been checked before calling this function, but it is necessary to do it in asynchronous code)
		$.fn.visage.preTransitionResize = function (image, values, group, index, visageDOM, isStopping, finish, options) {
			// Image has been loaded so there is no more need to display a loading sign
			if (loadingTimeout != null) {
				clearTimeout(loadingTimeout);
				loadingTimeout = null;
			}
			
			finish();
		};
		
		// We should check ((group != null) && (image != null) && !isStopping()) in an animation finish callback if we are using it
		// (It has been checked before calling this function, but it is necessary to do it in asynchronous code)
		$.fn.visage.postTransitionResize = function (image, values, group, index, visageDOM, isStopping, finish, options) {
			visageDOM.image.attr("src", values.src);
			
			finish();
		};
	})();
		
	var eventLock = 0;
	var visageDOM = {};
	var currentGroup = null;
	var currentIndex = -1;
	var currentImage = null;
	var currentOptions = null;
	var stopping = false;
	
	function start(index, group, options) {
		if (eventLock > 0) {
			return;
		}
		eventLock++;
		
		if (currentGroup != null) {
			// We are already displaying images
			
			if ((currentGroup == group) && (currentIndex != index)) {
				showImage(index);
			}
			
			eventLock--;
			return;
		}
		currentGroup = group;
		currentOptions = options;
		
		startDOM();
		
		// Hides Flash and other objects
		$("embed, object, select").css("visibility", "hidden"); // .hide() cannot be used
		
		eventLock++;
		currentOptions.showVisage(visageDOM, function () {
			return stopping;
		}, function () {
			showImage(index);
			eventLock--;
		}, currentOptions);
		
		eventLock--;
	};
	
	function stop() {
		if (stopping) {
			return;
		}
		stopping = true;
		
		eventLock++;
		
		currentOptions.beginStop(visageDOM, currentOptions);
		
		if (currentImage != null) {
			currentImage.onload();
			currentImage = null;
		}
		
		eventLock++;
		
		currentOptions.hideVisage(visageDOM, function () {
			// Shows Flash and other objects
			$("embed, object, select").css("visibility", "visible"); // .show() cannot be used
			
			stopDOM();
			
			currentGroup = null;
			currentIndex = -1;
			currentOptions = null;
			eventLock--;
			stopping = false;
		}, currentOptions);
		
		eventLock--;
	};
	
	function startDOM() {
		eventLock++;
		
		currentOptions.addDOM(visageDOM, currentOptions);
		
		$(visageDOM.overlay).add(visageDOM.close).unbind("click").click(function (event) {
			event.preventDefault();
			stop();
			return false;
		});
		
		$(visageDOM.prev).add(visageDOM.next).unbind("click");
				
		eventLock--;
	};
	
	function stopDOM() {
		eventLock++;
		
		currentOptions.removeDOM(visageDOM, currentOptions);
		visageDOM = {};
		
		eventLock--;
	};
	
	function showImage(index) {
		if ((currentGroup == null) || stopping) {
			return;
		}
		
		eventLock++;
		
		var image = currentGroup.eq(index);
		
		if (image == null) {
			eventLock--;
			return;
		}
		
		currentOptions.displayCount(index + 1, currentGroup.length, visageDOM, currentOptions);
		
		currentOptions.displayPrev(index + 1, currentGroup.length, visageDOM, currentOptions);
		
		if (index > 0) {
			visageDOM.prev.unbind("click").click(function (event) {
				event.preventDefault();
				if (eventLock == 0) {
					showImage(index - 1);
				}
				return false;
			});
		}
		else {			
			visageDOM.prev.unbind("click");
		}
		
		currentOptions.displayNext(index + 1, currentGroup.length, visageDOM, currentOptions);
		
		if (index < (currentGroup.length - 1)) {
			visageDOM.next.unbind("click").click(function (event) {
				event.preventDefault();
				if (eventLock == 0) {
					showImage(index + 1);
				}
				return false;
			});
		}
		else {
			visageDOM.next.unbind("click");
		}
		
		var imageValues = currentOptions.imageValues(image, currentOptions);
		
		// We checked stopping at the beginning of this function which does not take much until here so we will not check it again
		eventLock++;
		currentOptions.preImageLoad(imageValues, currentGroup, visageDOM, function () {
			return stopping;
		}, function () {
			if ((currentGroup != null) && (!stopping)) {
				eventLock++;
				currentImage = new Image();
				currentIndex = index;
				currentImage.onload = function () {
					this.onload = function () {};
					
					if ((currentGroup != null) && (currentImage != null) && (!stopping)) {
						preloadNeighbors(index);
						
						eventLock++;
						currentOptions.preTransitionResize(currentImage, imageValues, currentGroup, currentIndex, visageDOM, function () {
							return stopping;
						}, function () {
							resize (function () {
								if ((currentGroup != null) && (currentImage != null) && (!stopping)) {
									eventLock++;
									currentOptions.postTransitionResize(currentImage, imageValues, currentGroup, currentIndex, visageDOM, function () {
										return stopping;
									}, function () {
										eventLock--;
									}, currentOptions);
								}
							});
							
							eventLock--;
						}, currentOptions);
					}
					
					eventLock--;
				};
				currentImage.src = imageValues.src;
			}
			
			eventLock--;
		}, currentOptions);
			
		eventLock--;
	};
		
	function resize(postTransitionResize) {
		if ((currentGroup == null) || (currentImage == null) || stopping) {
			return;
		}
		
		eventLock++;
				
		var borderWidth = currentOptions.border.left + currentOptions.border.right;
		var borderHeight = currentOptions.border.top + currentOptions.border.bottom;
		
		var maxShareWidth = 1.0 - currentOptions.spaceAround.left - currentOptions.spaceAround.right;
		var maxShareHeight = 1.0 - currentOptions.spaceAround.top - currentOptions.spaceAround.bottom;
		
		var iWidth = currentImage.width + borderWidth;
		var iHeight = currentImage.height + borderHeight;
		
		// We make window size smaller for space around
		var wWidth = $(window).width() * maxShareWidth;
		var wHeight = $(window).height() * maxShareHeight;
		
		var wRatio = wWidth / wHeight;
		var iRatio = iWidth / iHeight;
		var ratio = wRatio / iRatio;
		
		// We start with an assumption that the image will cover the whole window (except for the space around)
		var size = 1.0;
		
		// Is the image small enough to display it with the original size?
		var originalSize = (iWidth <= wWidth) && (iHeight <= wHeight);
		
		if (originalSize) {
			// Makes target size smaller (as it is not needed that the image covers the whole window)
			size = size * Math.max(iWidth / wWidth, iHeight / wHeight);
		}
		
		if (ratio > 1) {
			// Variables have function scope
			var nWidth = size / ratio;
			var nHeight = size;
		}
		else {
			// Variables have function scope
			var nWidth = size;
			var nHeight = size * ratio;
		}
		
		// We need percents
		nWidth = (100.0 * maxShareWidth) * nWidth;
		nHeight = (100.0 * maxShareHeight) * nHeight;
		
		// We are centering the image
		var horizontal = ((100.0 * maxShareWidth) - nWidth) / 2.0;
		var vertical = ((100.0 * maxShareHeight) - nHeight) / 2.0;
		
		var css = {
			"left": (100.0 * currentOptions.spaceAround.left + horizontal) + "%",
			"right": (100.0 * currentOptions.spaceAround.right + horizontal) + "%",
			"top": (100.0 * currentOptions.spaceAround.top + vertical) + "%",
			"bottom": (100.0 * currentOptions.spaceAround.bottom + vertical) + "%"
		};
		if (originalSize) {
			// Border is not counted towards width and height
			css = $.extend(css, {"width": (iWidth - borderWidth) + "px", "height": (iHeight - borderHeight) + "px"});
		}
		else {
			css = $.extend(css, {"width": nWidth + "%", "height": nHeight + "%"});
		}
		
		eventLock++;
		currentOptions.resizeVisage(css, postTransitionResize != null, visageDOM,  function () {
			return stopping;
		}, function () {
			if (postTransitionResize != null) {
				postTransitionResize();
			}
			eventLock--;
		}, currentOptions);
		
		eventLock--;
	};

	function keyup(event) {
		if ((currentGroup == null) || (currentImage == null) || stopping) {
			return false;
		}
		
		var keycode = event.keyCode;
		var key = String.fromCharCode(keycode).toLowerCase();
		
		if ((currentOptions.keys.close && (key == currentOptions.keys.close)) || (keycode == (event.DOM_VK_ESCAPE || 27))) {
			stop();
			return true;
		}
		else if ((currentOptions.keys.prev && (key == currentOptions.keys.prev)) || (keycode == (event.DOM_VK_LEFT || 37))) {
			visageDOM.prev.click();
			return true;
		}
		else if ((currentOptions.keys.next && (key == currentOptions.keys.next)) || (keycode == (event.DOM_VK_RIGHT || 39))) {
			visageDOM.next.click();
			return true;
		}
		else if ((currentOptions.keys.first && (key == currentOptions.keys.first)) || (keycode == (event.DOM_VK_UP || 38))) {
			if (eventLock == 0) {
				showImage(0);
			}
			return true;
		}
		else if ((currentOptions.keys.last && (key == currentOptions.keys.last)) || (keycode == (event.DOM_VK_DOWN || 40))) {
			if (eventLock == 0) {
				showImage(currentGroup.length - 1);
			}
			return true;
		}
		
		return false;
	};
	
	function preloadNeighbors(index) {
		if ((currentGroup == null) || (currentImage == null) || stopping) {
			return;
		}
		
		try {
			if (index < (currentGroup.length - 1)) {
				var next = new Image();
				next.onload = function () {
					next.onload = function () {};
					next = null;
				};
				var image = currentGroup.eq(index + 1);
				next.src = currentOptions.imageValues(image, currentOptions).src;
			}
		}
		catch (e) {}
		
		try {
			if (index > 0) {
				var prev = new Image();
				prev.onload = function () {
					prev.onload = function () {};
					prev = null;
				};
				var image = currentGroup.eq(index - 1);
				prev.src = currentOptions.imageValues(image, currentOptions).src;
			}
		}
		catch (e) {}
	};

	function warn(message) {
		if ((typeof window.console != "undefined") && (typeof window.console.warn == "function")) {
			window.console.warn(message);
		}
	};
	
	// Extends $.support (the test needs document.body so we check it when DOM is ready)
	$(document).ready(function () {
		// Using test published by Juriy Zaytsev (kangax) on http://yura.thinkweb2.com/cft/
		$.support.positionFixed = false;
		if (document.createElement) {
			var el = document.createElement("div");
			if (el && el.style) {
				el.style.width = "1px";
				el.style.height = "1px";
				el.style.position = "fixed";
				el.style.top = "10px";
				var root = document.body;
				if (root && root.appendChild && root.removeChild) {
					root.appendChild(el);
					$.support.positionFixed = el.offsetTop === 10;
					root.removeChild(el);
				}
				el = null;
			}
		}
	});
	
	$(document).ready(function () {
		$(window).resize(function () {
			resize(null);
		});
		
		// We use keydown event and not keyup so that we can prevent browser handling events (like page scrolling on up/down keys)
		$(document).keydown(function (event) {
			if (keyup(event)) {
				event.preventDefault();
				return false;
			}
			else {
				return true;
			}
		});
	});
	
	$.fn.visage.defaults = {
		// Arrow and escape keys are always used, those are additional keys
		"keys": {
			"prev": "p",
			"next": "n",
			"close": "c",
			"first": "f",
			"last": "l"
		},
		"text": {
			"error": "Error displaying the image"
		},
		"files": {
			"blank": "./res/images/blank.gif",
			"error": "./res/images/error.png"
		},
		"css": {
			"close": {},
			"title": {},
			"count": {},
			"image": {},
			"container": {},
			"visage": {},
			"overlay": {},
			"prev": {},
			"prev_disabled": {},
			"next": {},
			"next_disabled": {}
		},
		"attr": {
			"close": {"id": "visage-close", "title": "Close"},
			"title": {"id": "visage-title"},
			"count": {"id": "visage-count"},
			"container": {"id": "visage-container"},
			"image": {"id": "visage-image", "alt": "", "title": "", "src": "./res/images/blank.gif"},
			"visage": {"id": "visage"},
			"overlay": {"id": "visage-overlay"},
			"prev": {"id": "visage-nav-prev", "title": "Previous"},
			"prev_disabled": {"id": "visage-nav-prev", "title": "Previous"},
			"next": {"id": "visage-nav-next", "title": "Next"},
			"next_disabled": {"id": "visage-nav-next", "title": "Next"}
		},
		
		"opacity": 0.9,
		"transitionResizeSpeed": 0, // in milliseconds
		"windowResizeSpeed": 300, // in milliseconds
		"onoffSpeed": 300, // in milliseconds
		"loadingWait": 100, // in milliseconds
		"border": {
			"left": 1,
			"right": 1,
			"top": 1,
			"bottom": 1
		}, // in pixels
		"spaceAround": {
			"left": 0.1,
			"right": 0.1,
			"top": 0.1,
			"bottom": 0.1
		}, // share of space
		"start": false, // do not autostart
		"registerEvents": true, // do register events
		"enabledClass": "visage-enabled",
		"disabledNavClass": "visage-nav-disabled",
		
		// We are calling functions in this way so the default functions can be redefined locally or globally
		"isSupported": function () { return $.fn.visage.isSupported.apply(this, arguments); },
		"addDOM": function () { return $.fn.visage.addDOM.apply(this, arguments); },
		"removeDOM": function () { return $.fn.visage.removeDOM.apply(this, arguments); },
		"displayCount": function () { return $.fn.visage.displayCount.apply(this, arguments); },
		"displayTitle": function () { return $.fn.visage.displayTitle.apply(this, arguments); },
		"displayNext": function () { return $.fn.visage.displayNext.apply(this, arguments); },
		"displayPrev": function () { return $.fn.visage.displayPrev.apply(this, arguments); },
		"imageValues": function () { return $.fn.visage.imageValues.apply(this, arguments); },
		"showVisage": function () { return $.fn.visage.showVisage.apply(this, arguments); },
		"hideVisage": function () { return $.fn.visage.hideVisage.apply(this, arguments); },
		"resizeVisage": function () { return $.fn.visage.resizeVisage.apply(this, arguments); },
		"beginStop": function () { return $.fn.visage.beginStop.apply(this, arguments); },
		"preImageLoad": function () { return $.fn.visage.preImageLoad.apply(this, arguments); },
		"preTransitionResize": function () { return $.fn.visage.preTransitionResize.apply(this, arguments); },
		"postTransitionResize": function () { return $.fn.visage.postTransitionResize.apply(this, arguments); }
	};
})(jQuery);
