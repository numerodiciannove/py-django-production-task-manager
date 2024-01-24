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
      $('#sidebar').toggleClass('active');
  });

})(jQuery);

function tableFilter(container, buttonClass, activeClass, defaultActive) {
    container = document.querySelector(container);
    if (!container) return;
    let buttons = container.querySelectorAll('.btn-group > button');
    let table = container.querySelector('table > tbody');

    [...buttons].forEach(el => {
        el.addEventListener('click', e => {
            [...buttons].forEach(button => {
                button.classList.remove(activeClass);
                button.classList.add(buttonClass);
            })

            el.classList.add(activeClass);
            el.classList.remove(buttonClass);

            let tr = [...table.querySelectorAll('tr')];
            tr.forEach(trEl => {
                trEl.classList.toggle('d-none', !trEl.classList.contains(el.dataset.status) && el.dataset.status !== 'all');
            })
        })

        if (el.dataset.status === defaultActive) {
            el.click()
        }
    })
}

tableFilter('.section_table_projects', 'btn-dark', 'btn-secondary', 'active-project');
tableFilter('.section_table_tasks', 'btn-dark', 'btn-secondary', 'incomplete-task');