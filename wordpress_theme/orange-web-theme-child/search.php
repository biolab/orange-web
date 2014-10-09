<?php
/**
 * The template for displaying search results pages.
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

							<?php if ( have_posts() ) : ?>

								<header class="page-header">
									<h1 class="title"><?php printf( __( 'Search results for &quot;%s&quot;', 'orange-web-theme' ), '<span>' . get_search_query() . '</span>' ); ?></h1>
								</header><!-- .page-header -->

								<?php /* Start the Loop */ ?>
								<?php while ( have_posts() ) : the_post(); ?>

									<?php
									/**
									 * Run the loop for the search to output the results.
									 * If you want to overload this in a child theme then include a file
									 * called content-search.php and that will be used instead.
									 */
									get_template_part( 'content', 'search' );
									?>

								<?php endwhile; ?>

								<?php orange_web_theme_paging_nav(); ?>

							<?php else : ?>

								<?php get_template_part( 'content', 'none' ); ?>

							<?php endif; ?>
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
