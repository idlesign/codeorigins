from collections import defaultdict

from ..settings import COUNTRIES, LANGUAGES, MIN_STARS, MIN_FOLLOWERS
from ..utils import logtime, LOG


class Fetcher:
    """Fetches data from GitHub."""

    name = None

    def __init__(self):
        self.results = {}

    def _gather_repos(self, language_name, min_stars):
        raise NotImplementedError

    def _gather_users(self, country_name, language_name, min_followers):
        raise NotImplementedError

    def run(self, languages=None, countries=None):
        """Fetches data from GitHub.

        Returns a dictionary indexed by country alias (iso code),
        where values are lists of Users.

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

                min_stars = language_meta.get('min_stars') or MIN_STARS

                with logtime('  Scanning `%s` repos. Min stars: %s' % (language, min_stars)):

                    for user_login, repo in self._gather_repos(language_name, min_stars):
                        repos[user_login].append(repo)

                with logtime('  Scanning `%s` users.  Min followers: %s' % (language, min_followers)):

                    for country in COUNTRIES:
                        if country not in countries:
                            continue

                        country_dict = results.setdefault(country, {})
                        users_list = country_dict.setdefault(language, [])

                        with logtime('    Scanning `%s` country users' % country):

                            for country_name in COUNTRIES[country]['names']:

                                for user_login, user in self._gather_users(country_name, language_name, min_followers):
                                    user_repos = repos.get(user_login, [])

                                    if user_repos:
                                        user.repos.extend(user_repos)
                                        users_list.append(user)
