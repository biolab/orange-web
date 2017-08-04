<?php
/**
 * Orange Web Theme functions and definitions
 *
 * @package Orange Web Theme
 */
function orange_web_theme_setup() {

	/*
	 * Make theme available for translation.
	 * Translations can be filed in the /languages/ directory.
	 * If you're building a theme based on Orange Web Theme, use a find and replace
	 * to change 'orange-web-theme' to the name of your theme in all the template files
	 */
	load_theme_textdomain( 'orange-web-theme', get_template_directory() . '/languages' );

	// Add default posts and comments RSS feed links to head.
	add_theme_support( 'automatic-feed-links' );

	/*
	 * Enable support for Post Thumbnails on posts and pages.
	 *
	 * @link http://codex.wordpress.org/Function_Reference/add_theme_support#Post_Thumbnails
	 */
	add_theme_support( 'post-thumbnails' );

	// This theme uses wp_nav_menu() in one location.
	register_nav_menus( array(
		'primary' => __( 'Primary Menu', 'orange-web-theme' ),
		'secondary' => __( 'Secondary Menu', 'orange-web-theme' ),
	) );

	/*
	 * Switch default core markup for search form, comment form, and comments
	 * to output valid HTML5.
	 */
	add_theme_support( 'html5', array(
		'search-form', 'comment-form', 'comment-list', 'gallery', 'caption',
	) );

	/*
	 * Enable support for Post Formats.
	 * See http://codex.wordpress.org/Post_Formats
	 */
	add_theme_support( 'post-formats', array(
		'aside', 'image', 'video', 'quote', 'link',
	) );

	// Setup the WordPress core custom background feature.
	add_theme_support( 'custom-background', apply_filters( 'orange_web_theme_custom_background_args', array(
		'default-color' => 'ffffff',
		'default-image' => '',
	) ) );
}

/**
 * Register widget area.
 *
 * @link http://codex.wordpress.org/Function_Reference/register_sidebar
 */
function orange_web_theme_widgets_init() {
	register_sidebar( array(
		'name'          => __( 'Orange Web Theme Sidebar', 'orange-web-theme' ),
		'id'            => 'sidebar-1',
		'description'   => '',
	    'before_widget' => '<aside id="%1$s" class="widget %2$s">',
		'after_widget'  => '</aside>',
		'before_title'  => '<h3 class="widget-title">',
		'after_title'   => '</h3>',
	) );
}
add_action( 'widgets_init', 'orange_web_theme_widgets_init' );

/**
 * Custom template tags for this theme.
 */
require get_theme_root() . '/orange-web-theme-child/inc/template-tags.php';
