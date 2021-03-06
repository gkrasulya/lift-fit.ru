/* Author: Georgy Krasulya

*/


jQuery.cookie=function(name,value,options){if(typeof value!='undefined'){options=options||{};if(value===null){value='';options.expires=-1;}
var expires='';if(options.expires&&(typeof options.expires=='number'||options.expires.toUTCString)){var date;if(typeof options.expires=='number'){date=new Date();date.setTime(date.getTime()+(options.expires*24*60*60*1000));}else{date=options.expires;}
expires='; expires='+date.toUTCString();}
var path=options.path?'; path='+(options.path):'';var domain=options.domain?'; domain='+(options.domain):'';var secure=options.secure?'; secure':'';document.cookie=[name,'=',encodeURIComponent(value),expires,path,domain,secure].join('');}else{var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}};


;(function($) {
	var $w = $(window),
		$b = $('body'),
		$slider = $('#slider');

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


	var $callbackForm = $('#callbackForm');

	if ($callbackForm) {
		$callbackForm.submit(function() {
			var $self = $(this);
			
			$self.find('button').html('Отправляется...').attr('disabled', true);

			if (emptyFiles) {

				if ($self.valid()) {
					$.post('/callback/', $self.serialize(), function(res) {
						$self.html('<p class="form-message">Мы перезвоним в ближайшее время!</p>');
					});
				}
				return false;

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
					refreshCart();
				} else {
					alert('Ошибка');
				}
			}
		});

		return false;
	});

	$('.js-favorites-to-cart').bind('click', function() {
		var $link = $(this),
			$product = $link.parents('.js-product'),
			id = $product.data('id'),
			inFavorites = $product.data('in-favorites') == '1',
			inCart = $product.data('in-cart') == '1';

		manageProduct(id, {
			inCart: 0,
			url: '/manage-cart/',

			success: function(res) {
				if (res && res.ok) {
					$product.fadeOut();

					refreshCart();
				} else {
					alert('Ошибка');
				}
			}
		});

		return false;
	})

	function manageProduct(id, opts) {
		opts = $.extend({
			success: function() {},
			error: function() {
				alert('Ошибка');
			},
			inCart: '1',
			inFavorites: 0,
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
					$('#bookmarks').html(res.html)
				}
			}
		});
	}

	var $cartTable = $('#cartTable'),
		$totalText = $('#totalText'),
		recountAllTotal = function() {
			var allTotal = 0,
				noPrice = false,
				text;

			$cartTable.find('.js-product').each(function(i, product) {
				var $product = $(product),
					price = $product.data('price');

				if (! price) {
					noPrice = true;
					return;
				}

				allTotal += price * $product.find('.js-quantity-input').val();
			});

			if (noPrice) {
				text = 'Итогую стоимость заказа мы укажем в коммерчеком предложении и вышлем на электронную почту.';
			} else {
				text = allTotal + ' руб.';
			}
			$totalText.html(text);
		};

	try {
		recountAllTotal();
	} catch(e) {}

	$('.js-quantity-plus, .js-quantity-minus').bind('click', function() {
		var $link = $(this),
			$wrap = $link.parent(),
			$product = $link.parents('.js-product'),
			price = $product.data('price'),
			$total = $product.find('.js-total'),
			$input = $wrap.find('.js-quantity-input'),
			quantity = +$input.val() + ($link.hasClass('js-quantity-plus') ? 1 : -1);
		if (quantity <= 0) {
			return false;
		}
		$total.html(price * quantity + ' руб.');
		$input.val(quantity);

		recountAllTotal();

		return false;
	});

	$('.js-remove-product').bind('click', function() {
		if (confirm('Вы уверены?')) {
			var $product = $(this).parents('.js-product'),
				inCart = $product.data('in-cart') || 1,
				inFavorites = $product.data('in-favorites') || 0;
			manageProduct($product.data('id'));
			$product.fadeOut('fast', function() {
				$product.remove();
				refreshCart();

				try {
					recountAllTotal();
				} catch(e) {}
			});
		}

		return false;
	});

	$(function() {
		refreshCart();
	});

	var $nameInput = $('#registerForm input[name=name]');

	if ($nameInput.length) {
		var $nameRow = $nameInput.parents('.form-row'),
			$overlay = $('<div id=overlay>');

		$nameInput.attr('tabIndex', 99);

		$overlay.css({
			width: $nameRow.width(),
			height: $nameRow.height(),
			background: 'url(/static/images/body.jpg)',
			position: 'absolute',
			left: 0,
			top: 0
		});
		$overlay.appendTo($nameRow);
	}


	var $scrollBody = $('html, body');

	var Navigation = {
		init: function() {
			if (window.PAGE !== 'MAIN') {
				return;
			}

			this.$nav = $('#nav');
			this.$links = $('a', this.$nav);

			this.$nav.on('click', 'a', $.proxy(this._onClick, this));

			this._checkSection();
		},

		_onClick: function(e) {
			e.stopPropagation();
			e.preventDefault();

			var $link = $(e.currentTarget),
				section = $link.data('section'),
				href = $link.attr('href');

			if ($link.data('link')) {
				document.location.href = href;
				return;
			}

			if ($link.hasClass('selected')) {
				return;
			}

			this.$links.removeClass('selected');
			$link.addClass('selected');

			this._scrollToSection(section);
			document.location.hash = 'section=' + section;

			return false;
		},

		_getLinkBySection: function(section) {
			return this.$links.filter('[data-section=' + section + ']');
		},

		_scrollToSection: function(section) {
			var $section = $('#' + section);

			$scrollBody.animate({
				scrollTop: $section.offset().top
			}, 250);
		},

		_checkSection: function() {
			var m = document.location.hash.match(/section=(about|catalog|delivery|howto|service)/),
				section = m ? m[1] : 'catalog';

			this.$links.removeClass('selected');
			this._getLinkBySection(section).addClass('selected');

			setTimeout($.proxy(function() {
				this._scrollToSection(section);
			}, this), 500);
		}
	};

	Navigation.init();

	var Carousel = {
		init: function() {
			this.$carousel = $('#carousel');
			this.$inner = $('.js-inner', this.$carousel);
			this.$items = $('.js-item', this.$carousel);

			this._length = this.$items.length;
			this._itemWidth = this.$items.outerWidth();
			this._maxLeft = 0;
			this._minLeft = -((this._length - 4) * this._itemWidth);
			this._currentLeft = 0;

			this.$carousel.on('click', '.js-arrow', $.proxy(this._onArrowClick, this));
		},

		_onArrowClick: function(e) {
			e.stopPropagation();
			e.preventDefault();

			var $arrow = $(e.currentTarget),
				direction = $arrow.data('direction');

			this._move(direction);
		},

		_move: function(direction) {
			var left = this._currentLeft + this._itemWidth * (direction === 'left' ? 1 : -1);

			if (left > this._maxLeft) {
				left = this._maxLeft;
			}
			if (left < this._minLeft) {
				left = this._minLeft;
			}

			this._currentLeft = left;
			this.$inner.stop().animate({
				marginLeft: left
			}, 200);
		}
	};

	Carousel.init();

	$('.fancybox').fancybox();

})(jQuery);
