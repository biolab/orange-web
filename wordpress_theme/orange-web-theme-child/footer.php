<?php
/**
 * The template for displaying the footer.
 *
 * Contains the closing of the #content div and all content after
 *
 * @package Orange Web Theme
 */
?>

	</div><!-- #content -->
	<!-- ******FOOTER****** -->
	<footer class="footer">
		<div class="container">
			<?php if (function_exists(orange_web_theme_secondary_menu())) orange_web_theme_secondary_menu(); ?>
			<!-- #lower site-navigation -->
			<small class="copyright pull-left">Copyright &copy; University of Ljubljana</small>
		</div>
	</footer>
	<!-- //******FOOTER****** -->
</div><!-- #page -->
<!-- Javascript files -->
<script type="text/javascript" src="<?php orange_web_home_url(); ?>/static/plugins/jquery-1.10.2.min.js"></script>
<script type="text/javascript" src="<?php orange_web_home_url(); ?>/static/plugins/jquery-migrate-1.2.1.min.js"></script>
<script type="text/javascript" src="<?php orange_web_home_url(); ?>/static/plugins/bootstrap/js/bootstrap.min.js"></script>
<script type="text/javascript" src="<?php echo get_stylesheet_directory_uri(); ?>/js/custom.js"></script>
<script type="text/javascript" src="<?php orange_web_home_url(); ?>/static/plugins/jquery-visage/src/jquery.visage.js"></script>
<script type="text/javascript" src="<?php orange_web_home_url(); ?>/static/plugins/jquery-visage/src/jquery.visage.init.js"></script>
<?php wp_footer(); ?>
<!-- Javascript end -->

</body>
</html>
