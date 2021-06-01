$(function() {
    $('.django-autocomplete-widget').each(function(_, widget) {
        $('li', widget).click(function(event) {
            $('input.django-autocomplete-key', widget).val($(this).data('key'));
            $('input.django-autocomplete-value', widget).val($(this).data('value'));
            $(widget).addClass('none');
            event.stopPropagation();
            event.preventDefault();
            return false;
        });


        $('input.django-autocomplete-value', widget).focusout(function(event) {
            setTimeout(function() { $(widget).addClass('none'); }, 200);
        });

        $('input.django-autocomplete-value', widget).keyup(function(event) {
            var input = this;

            if (event.keyCode == 38 || event.keyCode == 40) {
                var selected_index = -1;
                var active = $('li.active', widget);
                active.each(function (index, element) {
                    if ($(element).hasClass('selected'))
                        selected_index = index;
                });
                active.removeClass('selected');
                if (event.keyCode == 38) {
                    $(active[Math.max(selected_index - 1, 0)]).addClass('selected');
                } else {
                    $(active[Math.min(selected_index + 1, active.length - 1)]).addClass('selected');
                }

                event.stopPropagation();
                event.preventDefault();
                return false;
            }

            if (event.keyCode == 13) {
                var selected = $('li.active.selected', widget).first();
                $('input.django-autocomplete-key', widget).val(selected.data('key'));
                $(input).val(selected.data('value'));
                $('li.active', widget).first().addClass('selected');
                $(widget).addClass('none');

                event.stopPropagation();
                event.preventDefault();
                return false;
            }
            var value = $(input).val().toLowerCase();

            if (value.length == 0) {
                $('li', widget).removeClass('active').removeClass('selected');
                $(widget).addClass('none');
                return;
            }

            $('li', widget).each(function(_, item) {
                if ($(item).data('value').toLowerCase().indexOf(value) >= 0)
                    $(item).addClass('active');
                else
                    $(item).removeClass('active');
            });

            if ($('li.active.selected', widget).length == 0) {
                $('li', widget).removeClass('selected');
                $('li.active', widget).first().addClass('selected');
            }

            if ($('li.active', widget).length > 0)
                $(widget).removeClass('none');
            else
                $(widget).addClass('none');
        });

        $('input.django-autocomplete-value', widget).on('keyup keypress', function(event) {
            if (event.keyCode == 13) {
                event.stopPropagation();
                event.preventDefault();
                return false;
            }
        });
    });

    $('.django-widget-buttonselect, .django-widget-buttonselectinput').each(function(_, widget) {
        var multiple = $(widget)[0].hasAttribute('select-multiple');
        var input = $('input.django-widget-value', widget);
        var value = Array.from($('.btn.btn-success', widget).map(function(_, btn) { return $(btn).data('value'); })).join(',');
        input.val(value);

        widget.handle_click = function(event) {
            if (multiple) {
                $(this).toggleClass('btn-success').toggleClass('btn-default');
            } else {
                $('.btn', widget).removeClass('btn-success').addClass('btn-default');
                $(this).addClass('btn-success').removeClass('btn-default');
            }

            var value = Array.from($('.btn.btn-success', widget).map(function(_, btn) { return $(btn).data('value'); })).join(',');
            input.val(value);

            event.stopPropagation();
            event.preventDefault();
            return false;
        };

        $('.btn', widget).click(widget.handle_click);
    });

    $('.django-widget-buttonselectinput').each(function(_, widget) {
        $(".django-widget-new-item", widget).keypress(function(e) {
            if(e.which ==13) {
                var value = $(this).val().trim();
                var button = $('<button type="button" data-value="' + value + '" class="btn btn-default" >' + value + '</button>');
                button.click(widget.handle_click);
                $('.input-group-btn', widget).append(button);
                button.trigger('click');
                $(this).val('');
                e.preventDefault();
                return false;
            }
            e.stopPropagation();
        });
    });
});