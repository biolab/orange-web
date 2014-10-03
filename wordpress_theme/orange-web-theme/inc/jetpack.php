<?php
/**
 * Jetpack Compatibility File
 * See: http://jetpack.me/
 *
 * @package Orange Web Theme
 */

/**
 * Add theme support for Infinite Scroll.
 * See: http://jetpack.me/support/infinite-scroll/
 */
function orange_web_theme_jetpack_setup() {
	add_theme_support( 'infinite-scroll', array(
		'container' => 'main',
		'footer'    => 'page',
	) );
}
add_action( 'after_setup_theme', 'orange_web_theme_jetpack_setup' );
