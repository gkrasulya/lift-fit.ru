/* Author: Georgy Krasulya

*/

;(function() {
	var $w = $(window),
		$b = $('body'),
		$slider = $('#slider');

	if ($().nivoSlider) {
		$slider.nivoSlider({
			directionNav: false
		});
	}

	if(! Modernizr.input.placeholder) {
		$('input[placeholder], textarea[placeholder]').each(function(){
			var $this = $(this);

			if ($this.val() == '' && $this.attr('placeholder') != '') {
				$this.val($this.attr('placeholder'));
				$this.focus(function() {
					if ($this.val() == $this.attr('placeholder'))
						$this.val('');
				});

			$this.blur(function() {
				if ($this.val() == '') {
					$this.val($this.attr('placeholder'));
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
						$self.html('<p class="form-message">Спасибо за обратную связь!</p>');
					});
				}
				return false;

			}
		});
	}

	$('.js-add-to-cart').bind('click', function() {
		var $link = $(this),
			$product = $link.parents('.js-product'),
			id = $product.data('id'),
			inCart = $product.data('in-cart') == '1',
			inFavorites = $product.data('in-favorites') == '1';

		if (inFavorites && ! confirm('Вы уверены?')) {
			return false;
		}

		manageProduct(id, {
			inCart: inCart,
			url: '/manage-cart/',

			success: function(res) {
				if (res && res.ok) {
					if (inCart) {
						$product.data('in-cart', inCart ? '0' : '1');
						$link.html(inCart ? 'В корзину' : 'Из корзины');						
					} else {
						if (inFavorites) {
							$product.fadeOut('fast', function() {
								$product.remove();
							});
						}
						$link.replaceWith($('<a href="/order/cart/">В корзине</a>'));
					}

					refreshCart();
				} else {
					alert('Ошибка');
				}
			}
		});

		return false;
	});

	$('.js-add-to-favorites').bind('click', function() {
		var $link = $(this),
			$product = $link.parents('.js-product'),
			id = $product.data('id'),
			inFavorites = $product.data('in-favorites') == '1',
			inCart = $product.data('in-cart') == '1';

		if ((inFavorites || $link.data('remove')) && ! confirm('Вы уверены?')) {
			return false;
		}

		manageProduct(id, {
			url: '/manage-favorites/',
			inCart: inFavorites,

			success: function(res) {
				if (res && res.ok) {
					if (inFavorites || $link.data('remove')) {
						$product.fadeOut('fast', function() {
							$product.remove();
						});
					} else {
						$link.replaceWith($('<a href="/account/favorites/">В избранном</a>'));
					}
				} else {
					alert('Ошибка');
				}
			}
		});

		return false;
	});

	function manageProduct(id, opts) {
		opts = $.extend({
			success: function() {},
			error: function() {
				alert('Ошибка');
			},
			inCart: '1',
			url: '/manage-cart/'
		}, opts || {});

		$.ajax({
			url: opts.url,
			type: 'POST',
			data: {
				id: id,
				add: ! opts.inCart
			},
			dataType: 'json',

			success: opts.success,
			error: opts.error
		});		
	}

	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
		}
	});

	function refreshCart() {
		$.ajax({
			type: 'GET',
			dataType: 'json',
			url: '/get-cart/',
			success: function(res) {
				if (res && res.ok) {
					$('#headerCart').html(res.html)
				}
			}
		});
	}

	$('.js-quantity-plus, .js-quantity-minus').bind('click', function() {
		var $link = $(this),
			$wrap = $link.parent(),
			$input = $wrap.find('.js-quantity-input'),
			quantity = +$input.val() + ($link.hasClass('js-quantity-plus') ? 1 : -1);
		if (quantity <= 0) {
			return false;
		}
		$input.val(quantity);

		return false;
	});

	$('.js-remove-product').bind('click', function() {
		if (confirm('Sure?')) {
			var $product = $(this).parents('.js-product');
			manageProduct($product.data('id'));
			$product.fadeOut('fast', function() {
				$product.remove();
			});
		}

		return false;
	});

	$(function() {
		refreshCart();
	});

})();
