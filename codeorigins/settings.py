from .utils import sortdict


LANGUAGES = sortdict({

    'py': {
        'name': 'Python',
    },
    'go': {
        'name': 'Go',
    },
    'rust': {
        'name': 'Rust',
    },
    'c': {
        'name': 'C',
    },
    'java': {
        'name': 'Java',
    },
    'lisp': {
        'name': 'Lisp',
        'min_stars': 10,
    },

})
"""Supported programming languages."""


COUNTRIES = sortdict({

    'ru': {
        'names': ['Russia', 'Россия', 'Russian', 'RU'],
    },
    'by': {
        'names': ['Belarus', 'Беларусь', 'BY'],
    },
    'kz': {
        'names': ['Kazakhstan', 'Казахстан', 'KZ'],
    },
    'ua': {
        'names': ['Ukraine', 'Украина', 'Україна', 'UA'],
    },
    'cn': {
        'names': ['China', 'PRC', 'CN'],
    },
    'in': {
        'names': ['India', 'IN'],
    },
    'us': {
        'names': ['USA', 'United States', 'US'],
    },
    'au': {
        'names': ['Australia', 'AU'],
    },
    'uk': {
        'names': ['United Kingdom', 'GB', 'UK'],
    },
    'de': {
        'names': ['Germany', 'Deutschland', 'DE'],
    },
    'ca': {
        'names': ['Canada'],
        # CA is usually used for California.
    },
    'fr': {
        'names': ['France', 'FR'],
    },
    'br': {
        'names': ['Brazil', 'Brasil', 'BR'],
    },
    'mx': {
        'names': ['Mexico', 'México', 'MX'],
    },
    'ar': {
        'names': ['Argentina', 'Argentine', 'AR'],
    },
    'jp': {
        'names': ['Japan', '日本', 'JP'],
    },

})
"""Supported countries."""


MIN_FOLLOWERS = 5
"""Default minimum followers count for users."""


MIN_STARS = 20
"""Default minimum stars count for repositories."""

