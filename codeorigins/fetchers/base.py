from collections import defaultdict

from ..settings import COUNTRIES, LANGUAGES, MIN_FOLLOWERS
from ..utils import logtime, LOG, get_datetime_string


class Fetcher:
    """Fetches data from GitHub."""

    name = None

    def __init__(self):
        self.results = {}

    def _adjust_min_stars(self, language_name):
        raise NotImplementedError

    def _gather_repos(self, language_name, min_stars):
        raise NotImplementedError

    def _gather_users(self, country_name, language_name, min_followers):
        raise NotImplementedError

    def run(self, languages=None, countries=None):
        """Fetches data from GitHub.

        Stores a dictionary indexed by country alias (iso code),
        where values are lists of Users into ``self.results``.

        :param list languages: Filter. Language aliases .

        :param list countries: Filter. Country aliases.

        :rtype: dict

        """
        results = self.results

        languages = list(map(str.lower, languages or LANGUAGES.keys()))
        countries = list(map(str.lower, countries or COUNTRIES.keys()))

        repos = defaultdict(list)

        min_followers = MIN_FOLLOWERS

        with logtime('Running'):

            for language in LANGUAGES:
                if language not in languages:
                    continue

                language_meta = LANGUAGES[language]
                language_name = language_meta['name']

                LOG.info('  Adjusting `%s` min stars count ...', language_name)
                min_stars = self._adjust_min_stars(language_name)
                LOG.info('  Stars minimum set to %s', min_stars)

                with logtime('  Scanning `%s` repos. Min stars: %s' % (language, min_stars)):

                    for user_login, repo in self._gather_repos(language_name, min_stars):
                        user_repos = repos[user_login]

                        if repo not in user_repos:  # May double due to API limit bypass.
                            repos[user_login].append(repo)

                with logtime('  Scanning `%s` users.  Min followers: %s' % (language, min_followers)):

                    for country in COUNTRIES:
                        if country not in countries:
                            continue

                        users = {}

                        with logtime('    Scanning `%s` country users' % country):

                            for country_name in COUNTRIES[country]['names']:

                                for user_login, user in self._gather_users(country_name, language_name, min_followers):
                                    users.setdefault(user_login, user)

                            country_dict = results.setdefault(country, {})
                            lang_meta = country_dict.setdefault(language, {
                                'dt': get_datetime_string(),
                                'min_followers': min_followers,
                                'min_stars': min_stars,
                                'users': []
                            })
                            users_list = lang_meta['users']

                            for user_login, user in users.items():
                                user_repos = repos.get(user_login, [])

                                if user_repos:
                                    user.repos.extend(user_repos)
                                    users_list.append(user)
