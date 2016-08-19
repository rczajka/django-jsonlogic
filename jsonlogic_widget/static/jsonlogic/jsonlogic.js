(function($) {
  $.fn.jsonLogicEdit = function(options) {
    var editor = $('.jsonlogic-editor', this);
    var input = $('textarea', this);

    var operators = {
        '?:': {labels: ['if', 'then', 'else']},
        '!': {labels: ['!']},
        cat: {labels: ['cat', ',']},
        count: {labels: ['count', ',']},
        log: {labels: ['log', ',']},
        max: {labels: ['max', ',']},
        min: {labels: ['min', ',']},
    }

    function get_op_config(operator) {
        var cfg = {
            labels: ['', operator]
        }

        if (operator in operators)
            $.extend(cfg, operators[operator]);

        return cfg;
    }

    var menu = $('.jsonlogic-menu', editor);
    var container = $('.jsonlogic-container', editor);

    to_json = function(c) {
        var entry = $(c).children()

        if (entry.attr('data-jsonlogic-value')) {
            return JSON.parse(entry.attr('data-jsonlogic-value'))
        }
        if (entry.attr('data-jsonlogic-number')) {
            return parseFloat($("input", entry).val());
        }
        if (entry.attr('data-jsonlogic-string')) {
            return entry.text();
        }
        if (entry.attr('data-jsonlogic-operator') == 'var') {
            return {var: [entry.text()]}
        }
        if (entry.attr('data-jsonlogic-operator')) {
            var args = [];
            $("> .jsonlogic-container", entry).each(function(i, e) {
                args.push(to_json(e));
            });
            var v = {};
            v[entry.attr('data-jsonlogic-operator')] = args
            return v
        }
    }

    menu.on("click", ".jsonlogic-submenu-header", function() {
        $(".active", menu).removeClass("active")
        $(this).parent().addClass("active")
        return false
    });
    menu.on("click", ".jsonlogic-button", function() {
        drawIn(
            $('.active', container).parent(),
            JSON.parse($(this).attr('data-jsonlogic'))
        )
        input.text(JSON.stringify(to_json(container)))
    });

    container.on("click", ".jsonlogic", function() {
        $(".active", container).removeClass("active")
        $(this).addClass("active")
        return false
    });

    container.on("change", "input", function() {
        input.text(JSON.stringify(to_json(container)))
    });

    var root = JSON.parse(input.val() || "null");

    function drawIn(container, value) {
        container.text('');
        var $elem = $("<div class='jsonlogic'></div>");
        $elem.appendTo(container)

        if (value === null) {
            $elem.attr("data-jsonlogic-value", 'null');
            $elem.text('null');
            $elem.addClass('jsonlogic-const');
        } else if (value === true) {
            $elem.attr("data-jsonlogic-value", 'true');
            $elem.text('true');
            $elem.addClass('jsonlogic-const');
        } else if (value === false) {
            $elem.attr("data-jsonlogic-value", 'false');
            $elem.text('false');
            $elem.addClass('jsonlogic-const');
        } else if (typeof value === "number") {
            $elem.attr("data-jsonlogic-number", "true");
            $elem.addClass("jsonlogic-number")
            $input = $("<input value='" + value + "'>")
            $input.appendTo($elem)
        } else if (typeof value === "string") {
            $elem.attr("data-jsonlogic-string", "true");
            $elem.addClass("jsonlogic-action")
            $elem.text(value)
        } else if ('var' in value) {
            $elem.attr("data-jsonlogic-operator", "var");
            $elem.addClass("jsonlogic-variable");
            $.each(value["var"], function(i, elem) {
                if (i) {
                    $elem.append("; default: ")
                    $item = $("<div class='jsonlogic-container'></div>")
                    $elem.append($item)
                    drawIn($item, elem)
                } else {
                    $elem.append(elem)
                }
            });
        } else {
            operator = Object.keys(value)[0];
            var cfg = get_op_config(operator)
            $elem.addClass("jsonlogic-operator");

            $elem.attr("data-jsonlogic-operator", operator);

            $.each(value[operator], function(i, elem) {
                $elem.append(cfg.labels[Math.min(i, cfg.labels.length - 1)])
                $item = $("<div class='jsonlogic-container'></div>")
                $elem.append($item)
                drawIn($item, elem)
            });
        }

    }

    editor.on("click", ".jsonlogic-submenu-header")

    drawIn(container, root);
  };

    $(function() {
        $(".jsonlogic-field").each(function() {
            $(this).jsonLogicEdit()
        });
        $(document).on("formset:added", function() {
            $(".jsonlogic-field", this).each(function() {
                $(this).jsonLogicEdit()
            });
        });
    })

})(django.jQuery);
