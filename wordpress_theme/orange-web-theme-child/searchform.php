<form role="search" method="get" class="search-form form-inline" action="<?php echo home_url( '/' ); ?>">
	<div class="form-group">
		<label class="sr-only screen-reader-text"><?php echo _x( 'Quick search', 'label' ) ?></label>
		<input type="search" class="search-field" placeholder="<?php echo esc_attr_x( 'Search …', 'placeholder' ) ?>" value="<?php echo get_search_query() ?>" name="s" title="<?php echo esc_attr_x( 'Quick search', 'label' ) ?>" />
		<input type="submit" class="search-submit" value="<?php echo esc_attr_x( 'Go', 'submit button' ) ?>" />
  	</div>
</form>
