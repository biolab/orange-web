<?php
/**
 * Custom template tags for this theme.
 *
 * Eventually, some of the functionality here could be replaced by core features.
 *
 * @package Orange Web Theme
 */

/**
* Main homepage
*/
$web_home_url = 'http://new.orange.biolab.si';

function orange_web_home_url() {
	echo esc_url( $GLOBALS['web_home_url'] );
}

/**
 * Primary menu
 */
function orange_web_theme_primary_menu() {
	$menu_name = 'primary'; // specify custom menu slug
	if (($locations = get_nav_menu_locations()) && isset($locations[$menu_name])) {
		$menu = wp_get_nav_menu_object($locations[$menu_name]);
		$menu_items = wp_get_nav_menu_items($menu->term_id);

		$menu_list = '<div class="navbar-collapse collapse" id="navbar-collapse">' ."\n";
		$menu_list .= '    <ul class="nav navbar-nav">' ."\n";
		$menu_list .= '        <li class="active nav-item sr-only"><a href="' . $GLOBALS['web_home_url'] .'">Home</a></li>' ."\n";
		foreach ((array) $menu_items as $key => $menu_item) {
			$title = $menu_item->title;
			$url = $menu_item->url;
			$menu_list .= '        <li class="nav-item"><a href="'. $url .'">'. $title .'</a></li>' ."\n";
		}
		$menu_list .= '    </ul>' ."\n";
		$menu_list .= '</div>' ."\n";
	} else {
		// $menu_list = '<!-- no list defined -->';
	}
	echo $menu_list;
}

/**
 * Secondary menu
 */
function orange_web_theme_secondary_menu() {
	$menu_name = 'secondary'; // specify custom menu slug
	if (($locations = get_nav_menu_locations()) && isset($locations[$menu_name])) {
		$menu = wp_get_nav_menu_object($locations[$menu_name]);
		$menu_items = wp_get_nav_menu_items($menu->term_id);

		$menu_list = '<ul class="links list-inline pull-right">' ."\n";
		foreach ((array) $menu_items as $key => $menu_item) {
			$title = $menu_item->title;
			$url = $menu_item->url;
			$menu_list .= '    <li><a href="'. $url .'">'. $title .'</a></li>' ."\n";
		}
		$menu_list .= '</ul>' ."\n";
	} else {
		// $menu_list = '<!-- no list defined -->';
	}
	echo $menu_list;
}

function orange_web_theme_entry_footer() {
	// Hide category and tag text for pages.
	if ( 'post' == get_post_type() ) {
		/* translators: used between list items, there is a space after the comma */
		$tags_list = get_the_tag_list( '', __( ', ', 'orange-web-theme' ) );
		if ( $tags_list ) {
			printf( '<span class="tags-links">' . __( 'Tags: %1$s', 'orange-web-theme' ) . '</span>', $tags_list );
		}
	}
}

/**
 * Display navigation to next/previous post when applicable.
 */
function orange_web_theme_post_nav() {
	// Don't print empty markup if there's nowhere to navigate.
	$previous = ( is_attachment() ) ? get_post( get_post()->post_parent ) : get_adjacent_post( false, '', true );
	$next     = get_adjacent_post( false, '', false );

	if ( ! $next && ! $previous ) {
		return;
	}
	?>
	<nav class="navigation post-navigation" role="navigation">
		<h3 class="screen-reader-text sr-only"><?php _e( 'Post navigation', 'orange-web-theme' ); ?></h3>
		<div class="nav-links">
			<?php
				previous_post_link( '<div class="nav-previous">%link</div>', _x( '<span class="meta-nav">&larr;</span>&nbsp;%title', 'Previous post link', 'orange-web-theme' ) );
				next_post_link(     '<span> | </span><div class="nav-next">%link</div>',     _x( '%title&nbsp;<span class="meta-nav">&rarr;</span>', 'Next post link',     'orange-web-theme' ) );
			?>
		</div><!-- .nav-links -->
	</nav><!-- .navigation -->
	<?php
}

/**
 * Display navigation to next/previous set of posts when applicable.
 */
function orange_web_theme_paging_nav() {
	// Don't print empty markup if there's only one page.
	if ( $GLOBALS['wp_query']->max_num_pages < 2 ) {
		return;
	}
	?>
	<nav class="navigation paging-navigation" role="navigation">
		<h3 class="screen-reader-text sr-only"><?php _e( 'Page navigation', 'orange-web-theme' ); ?></h3>
		<div class="nav-links">

				<?php if ( get_next_posts_link() ) : ?>
				<div class="nav-previous"><?php next_posts_link( __( '<span class="meta-nav">&larr;</span> Older posts', 'orange-web-theme' ) ); ?></div>
				<?php endif; ?>

				<?php if ( get_previous_posts_link() ) : ?>
				<?php _e( '<span> | </span>', 'orange-web-theme' ); ?><div class="nav-next"><?php previous_posts_link( __( 'Newer posts <span class="meta-nav">&rarr;</span>', 'orange-web-theme' ) ); ?></div>
				<?php endif; ?>

		</div><!-- .nav-links -->
	</nav><!-- .navigation -->
	<?php
}
/**
 * Prints HTML with meta information for the current post-date/time and author.
 */
function orange_web_theme_posted_on() {
	$time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';

	$time_string = sprintf( $time_string,
		esc_attr( get_the_date( 'c' ) ),
		esc_html( get_the_date() ),
		esc_attr( get_the_modified_date( 'c' ) ),
		esc_html( get_the_modified_date() )
	);

	$posted_on = sprintf(
		_x( 'Posted: %s', 'post date', 'orange-web-theme' ),
		'<a href="' . esc_url( get_permalink() ) . '" rel="bookmark">' . $time_string . '</a>'
	);

	$byline = sprintf(
		_x( 'Author: %s', 'post author', 'orange-web-theme' ),
		'<span class="author vcard"><a class="url fn n" href="' . esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ) . '">' . esc_html( get_the_author() ) . '</a></span>'
	);

	$sep = sprintf('<span> | </span>');

	echo '<span class="posted-on">' . $posted_on . '</span>' . $sep . '<span> ' . $byline . '</span>';
	edit_post_link( __( 'Edit', 'orange-web-theme' ), $sep . '<span class="edit-link">', '</span>' );

	if ( ! is_single() && ! post_password_required() && ( comments_open() || get_comments_number() ) ) {
		echo '<span class="comments-link">';
		comments_popup_link( __( 'Leave a comment', 'orange-web-theme' ), __( '1 Comment', 'orange-web-theme' ), __( '% Comments', 'orange-web-theme' ) );
		echo '</span>';
	}
}
