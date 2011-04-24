/* Author: Gosha Krasulya
	
*/

(function(){

	var $icons = $('#icons a');

	$icons.hover(function() {
		$(this).stop().animate({
			'top': 3
		}, 100);
	},
	function() {
		$(this).stop().animate({
			'top': 0
		}, 100);
	});



	var $sideNav = $('#sideNav');

	$sideNav.find('a').hover(function() {
		var $self = $(this);

		$self.stop().animate({
			'background-color': '#ff0',
			'margin-left': 10
		}, 100);
	}, function() {
		var $self = $(this);

		$self.stop().animate({
			'background-color': '#d9e8f1',
			'margin-left': 0
		}, 400);
	});



	var $content = $('#content'),
		$mainBar = $('#mainBar'),
		$w = $(window);

	$w.resize(windowResizeHandler);

	function windowResizeHandler() {
		setContentWidth();
		setMainBarWidth();
	}

	setContentWidth();
	setMainBarWidth();

	function setContentWidth() {
		$content.width() < 1000 && $content.width(1000);
	}

	function setMainBarWidth() {
		$mainBar.width($content.width() - 630);
	}


	var $feedbackForm = $('#feedbackForm');

	if ($feedbackForm.length) {

		var validateOptions = {
			'rules': {
				'name': 'required',
				'body': 'required'
			},
			'messages': {
				'name': 'Пожалуйста, введите ваше имя',
				'body': 'Сообщение не может быть пустым'
			},
			'errorClass': 'invalid'
		},
			$file = $feedbackForm.find('input[type=file]'),
			emptyFiles = true,
			currentFile = 1,
			$formLastChild;

		$file.change(fileChangeHandler);

		function fileChangeHandler() {
			emptyFiles = false;
			currentFile++;
			var $newFileInput = $('<p class="file"><input type="file" name="attachment' + currentFile + '"</p>'),
				$p = $(this).parents('p:eq(0)');
			! $p.next().hasClass('file') && $newFileInput.insertAfter($p);

			$newFileInput.find('input').change(fileChangeHandler);
		}

		$feedbackForm.validate(validateOptions);

		$feedbackForm.submit(function() {
			var $self = $(this);
			
			$self.find('button').html('Отправляется...').attr('disabled', true);

			if (emptyFiles) {

				if ($self.valid()) {
					$.post('/feedback/', $self.serialize(), function(res) {
						$self.html('<p class="b-message">Спасибо за обратную связь!</p>');
					});
				}
				return false;

			}
		});

	}


})();









