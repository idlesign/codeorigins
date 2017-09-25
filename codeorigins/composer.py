from collections import defaultdict, OrderedDict
from datetime import datetime, timezone
from operator import itemgetter
from os import getcwd

from .settings import COUNTRIES, LANGUAGES
from .utils import Renderer


class HtmlComposer:
    """Offers export to HTML functions."""

    max_users = 25
    max_repos = 50

    def __init__(self, data):
        """
        :param dict data: Expected Dumper.read() result.
        """
        self.data = data

    def make_html(self, target_dir=None):
        """Compiles HTML from the data and puts it into a target directory.

        :param str target_dir: If not set current working dir is used.

        """
        target_dir = target_dir or getcwd()
        data = self.data

        def sort_by_stars(what):
            what.sort(key=itemgetter('stars'), reverse=True)

        for language, countries in data.items():

            ctx_users = []
            ctx_repos = []
            ctx_countries = defaultdict(int)

            for country, users in countries.items():

                for user in users:

                    user_stars = 0

                    for repo in user.repos:
                        stars = repo.stars
                        user_stars += stars

                        ctx_repos.append({
                            'country': country,
                            'user': user.name,
                            'stars': stars,
                            'info': repo,
                        })
                        ctx_countries[country] += stars

                    ctx_users.append({
                        'country': country,
                        'stars': user_stars,
                        'info': user,
                    })

            sort_by_stars(ctx_users)
            sort_by_stars(ctx_repos)
            ctx_countries = OrderedDict(sorted(ctx_countries.items(), key=lambda item: item[1], reverse=True))

            Renderer.render_to_directory('page.html', target_dir, {
                'language': language,
                'users': ctx_users,
                'repos': ctx_repos,
                'countries': ctx_countries,
                'max_users': self.max_users,
                'max_repos': self.max_repos,
                'all_countries': COUNTRIES,
                'all_languages': LANGUAGES,
                'dt_compiled': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M'),
            }, target_filename='page_%s.html' % language)
