(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
	// $('#collapseButton').removeClass('fa fa-bars');
	$('#collapseButton').toggleClass('fa-bars  ');
      $('#sidebar').toggleClass('active');
  });
 
})(jQuery);
