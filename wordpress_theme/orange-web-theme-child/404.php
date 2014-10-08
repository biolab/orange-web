<?php
/**
 * The template for displaying 404 pages (not found).
 *
 * @package Orange Web Theme
 */

get_header(); ?>
	<div id="primary" class="content-area">
		<main id="main" class="site-main" role="main">
			<section id="features" class="features section custom-reduce-padding-2">
		        <div class="container">
		            <div class="row">
		            	<div class="col-md-9 col-sm-7 col-xs-12 documentwrapper">
							<section class="error-404 not-found">
								<header class="page-header">
									<h1 class="title"><?php _e( 'Oops! That page can&rsquo;t be found.', 'orange-web-theme' ); ?></h1>
								</header><!-- .page-header -->

								<div class="content">
									<p><?php _e( 'It looks like nothing was found at this location. Maybe try one of the links below or the sidebar?', 'orange-web-theme' ); ?></p>

									<?php the_widget( 'WP_Widget_Recent_Posts' ); ?>

									<?php if ( orange_web_theme_categorized_blog() ) : // Only show the widget if site has multiple categories. ?>
									<div class="widget widget_categories">
										<h2 class="widget-title"><?php _e( 'Most Used Categories', 'orange-web-theme' ); ?></h2>
										<ul>
										<?php
											wp_list_categories( array(
												'orderby'    => 'count',
												'order'      => 'DESC',
												'show_count' => 1,
												'title_li'   => '',
												'number'     => 10,
											) );
										?>
										</ul>
									</div><!-- .widget -->
									<?php endif; ?>

									<?php
										/* translators: %1$s: smiley */
										$archive_content = '<p>' . sprintf( __( 'Try looking in the monthly archives. %1$s', 'orange-web-theme' ), convert_smilies( ':)' ) ) . '</p>';
										the_widget( 'WP_Widget_Archives', 'dropdown=1', "after_title=</h2>$archive_content" );
									?>

								</div><!-- .page-content -->
							</section><!-- .error-404 -->
						</div>
						<div class="col-md-3 col-sm-5 col-xs-12">
							<?php get_sidebar(); ?>
						</div>
					</div><!--//row-->
		        </div><!--//container-->
		    </section><!--//features section document-->
		</main><!-- #main -->
	</div><!-- #primary -->
<?php get_footer(); ?>
