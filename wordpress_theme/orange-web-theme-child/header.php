<?php
/**
 * The header for our theme.
 *
 * Displays all of the <head> section and everything up till <div id="content">
 *
 * @package Orange Web Theme
 */
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Orange Data Mining Toolbox">
<meta name="author" content="Bioinformatics Laboratory, University of Ljubljana">
<title><?php wp_title( '|', true, 'right' ); ?></title>
<!-- <link rel="profile" href="http://gmpg.org/xfn/11">*/ -->
<link rel="pingback" href="<?php bloginfo( 'pingback_url' ); ?>">
<link rel="shortcut icon" href="<?php orange_web_home_url(); ?>/static/images/favicon.ico">
<link rel="stylesheet" href="<?php orange_web_home_url(); ?>/static/plugins/bootstrap/css/bootstrap.min.css">
<?php wp_head(); ?>
<link rel="stylesheet" href="<?php orange_web_home_url(); ?>/static/plugins/font-awesome/css/font-awesome.css">
<link rel="stylesheet" href="<?php orange_web_home_url(); ?>/static/plugins/jquery-visage/res-alt/visage.css">
<link rel="stylesheet" href="<?php orange_web_home_url(); ?>/static/css/styles.css">
<link rel="stylesheet" href="<?php orange_web_home_url(); ?>/static/css/custom.css">
<!-- External fonts -->
<link href='https://fonts.googleapis.com/css?family=Lato:300,400,700,300italic,400italic,700italic' rel='stylesheet' type='text/css'>
<link href='https://fonts.googleapis.com/css?family=Covered+By+Your+Grace' rel='stylesheet' type='text/css'>
<!-- Global CSS -->
</head>

<body <?php body_class(); ?>>
<div id="page" class="hfeed site">
	<a class="skip-link screen-reader-text sr-only" href="#content"><?php _e( 'Skip to content', 'orange-web-theme' ); ?></a>

	<header id="top" class="header navbar-fixed-top" role="banner">
		<div class="container">
			<h1 class="logo pull-left">
	            <a href="https://orange.biolab.si/">
	                <img id="logo-image" class="logo-image" src="<?php orange_web_home_url(); ?>/static/images/orange-logo-w.png" alt="Logo">
	            </a>
	        </h1><!--//logo-->

			<nav id="main-nav" class="main-nav navbar-right" role="navigation">
				<div class="navbar-header">
	                <button class="navbar-toggle" type="button" data-toggle="collapse" data-target="#navbar-collapse">
	                    <span class="sr-only">Toggle navigation</span>
	                    <span class="icon-bar"></span>
	                    <span class="icon-bar"></span>
	                    <span class="icon-bar"></span>
	                </button><!--//nav-toggle-->
	            </div><!--//navbar-header-->
				<?php if (function_exists(orange_web_theme_primary_menu())) orange_web_theme_primary_menu(); ?>
			</nav><!-- #upper site-navigation -->
		</div>
	</header><!-- #masthead -->

	<div id="content" class="site-content">
