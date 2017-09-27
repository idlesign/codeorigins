/* globals $ */


function applyCountryFilters() {
    "use strict";

    var chosenCountries = [];

    $.each($('.cb-country'), function (idx, el) {
        if (el.checked) {
            chosenCountries.push($(el).data('name'));
        }
    });

    function applyTo(selector) {
        $.each($(selector), function (idx, el) {
            var $row = $(el),
                country = $row.data('country');

            if ($.inArray(country, chosenCountries) > -1) {
                $row.show();
            } else {
                $row.hide();
            }
        });
    }

    applyTo('.row-user');
    applyTo('.row-repo');
}

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

            window.githubCard.render($card.get(0), 'https://lab.lepture.com/github-cards/cards/default.html');

            return $container.html();
        },
        'delay': {show: 500, hide: 10 },
        'html': true,
        'trigger': 'hover'
    });

    $('.cb-country').on('click', applyCountryFilters);

});
