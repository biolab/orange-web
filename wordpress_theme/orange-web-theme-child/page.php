<?php
/**
 * The template for displaying all pages.
 *
 * This is the template that displays all pages by default.
 * Please note that this is the WordPress construct of pages
 * and that other 'pages' on your WordPress site will use a
 * different template.
 *
 * @package Orange Web Theme
 */

get_header(); ?>
	<div id="primary" class="content-area">
		<main id="main" class="site-main" role="main">
			<section id="features" class="features section custom-reduce-padding-2">
		        <div class="container">
		            <div class="row">
		            	<div class="col-lg-9 col-md-8 col-sm-7 col-xs-12 documentwrapper">
							<?php while ( have_posts() ) : the_post(); ?>

								<?php get_template_part( 'content', 'page' ); ?>

								<?php
									// If comments are open or we have at least one comment, load up the comment template
									if ( comments_open() || '0' != get_comments_number() ) :
										comments_template();
									endif;
								?>

							<?php endwhile; // end of the loop. ?>
						</div>
						<div class="col-lg-3 col-md-4 col-sm-5 col-xs-12">
							<?php get_sidebar(); ?>
						</div>
					</div><!--//row-->
		        </div><!--//container-->
		    </section><!--//features section document-->
		</main><!-- #main -->
	</div><!-- #primary -->
<?php get_footer(); ?>
