from .utils import sortdict


LANGUAGES = sortdict({

    'py': {
        'name': 'Python',
    },
    'asm': {
        'name': 'Assembly',
    },
    'ruby': {
        'name': 'Ruby',
    },
    'objc': {
        'name': 'Objective-C',
    },
    'swift': {
        'name': 'Swift',
    },
    'shell': {
        'name': 'Shell',
    },
    'php': {
        'name': 'PHP',
    },
    'js': {
        'name': 'JavaScript',
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
    'gb': {
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


MIN_FOLLOWERS = 10
"""Default minimum followers count for users."""


STARS_BASE = 25
"""Stars count for repositories to star with."""


STARS_MIN = 15
"""Minimal number of stars."""


REPOS_BASE = 30000
"""Base repository number for a language to adjust stars count."""

