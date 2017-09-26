/* globals $ */

$(function () {
    "use strict";

    $('[data-toggle="tooltip"]').tooltip();

    $('.card-popover').popover({
        'content': function() {
            var $el = $(this),
                val = $el.data('card'),
                $container = $('<div>'),
                $card = $('<div class="github-card" data-github="' + val + '"></div>');

            $container.append($card);

            window.githubCard.render($card.get(0), 'http://lab.lepture.com/github-cards/cards/default.html');

            return $container.html();
        },
        'delay': {show: 500, hide: 10 },
        'html': true,
        'trigger': 'hover'
    });

});
