/* Author: Georgy Krasulya

*/

;(function() {
	var $slider = $('#slider');

	$slider.nivoSlider({
		directionNav: false
	});

	if(!Modernizr.input.placeholder) {
		$('input[placeholder], textarea[placeholder]').each(function(){
			if ($(this).val() == '' && $(this).attr('placeholder') != '') {
				$(this).val($(this).attr('placeholder'));
				$(this).focus(function() {
					if ($(this).val() == $(this).attr('placeholder'))
						$(this).val('');
				});

			$(this).blur(function() {
				if ($(this).val() == '') {
					$(this).val($(this).attr('placeholder'));
				}
			});
			}
		});
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
			var $newFileInput = $('<p class="file mt5"><input type="file" name="attachment' + currentFile + '"</p>'),
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
