from ..settings import COUNTRIES, LANGUAGES, MIN_STARS, MIN_FOLLOWERS
from ..utils import logtime


class Fetcher:
    """Fetches data from GitHub."""

    name = None

    def _gather(self, country, language, min_stars, min_followers, totals_only=False):
        raise NotImplementedError

    def run(self, languages=None, countries=None, totals_only=False):
        """Fetches data from GitHub.

        Returns a dictionary indexed by country alias (iso code),
        where values are lists of Users.

        :param list languages: Filter. Language aliases .

        :param list countries: Filter. Country aliases.

        :param bool totals_only: Don't fetch stats. Only log total users.

        :rtype: dict

        """
        results = {}

        languages = list(map(str.lower, languages or LANGUAGES.keys()))
        countries = list(map(str.lower, countries or COUNTRIES.keys()))

        with logtime('* Run'):

            for country in COUNTRIES:
                if country not in countries:
                    continue

                with logtime(' * Country `%s`' % country):

                    country_dict = results.setdefault(country, {})

                    for language in LANGUAGES:
                        if language not in languages:
                            continue

                        language_meta = LANGUAGES[language]
                        language_name = language_meta['name']

                        min_stars = language_meta.get('min_stars') or MIN_STARS
                        min_followers = MIN_FOLLOWERS

                        with logtime('  * Language `%s`' % language):
                            users_list = country_dict.setdefault(language, [])

                            for country_name in COUNTRIES[country]['names']:

                                users = self._gather(
                                    country_name, language_name,
                                    min_stars=min_stars,
                                    min_followers=min_followers,
                                    totals_only=totals_only)

                                users and users_list.extend(users)

        return results
