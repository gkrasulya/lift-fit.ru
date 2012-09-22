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



	var $wr = $('.l-wrapper'),
		$content = $('#content'),
		$mainBar = $('#mainBar'),
		$w = $(window),
		$spareList = $('#spareList');




	typeof $().fancybox != 'undefined'
		&& $spareList.find('a').fancybox();

	$w.resize(windowResizeHandler);

	function windowResizeHandler() {
		setContentWidth();
		setMainBarWidth();
		setSpareListWidth();
	}

	setContentWidth();
	setMainBarWidth();
	setSpareListWidth();

	function setContentWidth() {
		$wr.width() < 932 && $wr.width(932);
		$content.width() < 932 && $content.width(932);
	}

	function setMainBarWidth() {
		$mainBar.width($content.width() - 630);
	}

	function setSpareListWidth() {
		var baseWidth = $w.width() < 932 ? 932 : $w.width(),
			width = (baseWidth / 1.45) - (100 / (Math.pow(baseWidth / 932, 2)));
		$spareList.width(width);
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









