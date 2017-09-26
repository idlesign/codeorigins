from collections import defaultdict, OrderedDict
from datetime import datetime, timezone
from operator import itemgetter
from os import makedirs, path, getcwd

from .settings import COUNTRIES, LANGUAGES
from .utils import Renderer, LOG


class HtmlComposer:
    """Offers export to HTML functions."""

    max_users = 50
    max_repos = 200

    def __init__(self, data):
        """
        :param dict data: Expected Dumper.read() result.
        """
        self.data = data

    def make_html(self, target_dir=None):
        """Compiles HTML from the data and puts it into a target directory.

        :param str target_dir: If not set current working dir is used.

        """
        if target_dir is None:
            target_dir = path.join(getcwd(), 'docs')
            makedirs(target_dir, exist_ok=True)

        LOG.info('Generating HTML in %s ...', target_dir)

        data = self.data
        compilation_date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')

        def sort_by_stars(what):
            """
            :param list|dict what:
            :rtype: list|dict
            """
            if isinstance(what, list):
                return sorted(what, key=itemgetter('stars'), reverse=True)

            return OrderedDict(sorted(what.items(), key=lambda item: item[1], reverse=True))

        def add_common_context(ctx):
            ctx.update({
                'all_countries': COUNTRIES,
                'all_languages': LANGUAGES,
                'dt_compiled': compilation_date,
            })
            return ctx

        index_languages = defaultdict(int)
        index_countries = defaultdict(int)

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

                        index_languages[language] += stars
                        index_countries[country] += stars

                    ctx_users.append({
                        'country': country,
                        'stars': user_stars,
                        'info': user,
                    })

            target_filename = 'page_%s.html' % language

            LOG.info('  Writing %s ...', target_filename)

            Renderer.render_to_directory('page.html', target_dir, add_common_context({
                'subtitle': LANGUAGES[language]['name'],
                'users': sort_by_stars(ctx_users),
                'repos': sort_by_stars(ctx_repos),
                'countries': sort_by_stars(ctx_countries),
                'max_users': self.max_users,
                'max_repos': self.max_repos,
            }), target_filename=target_filename)

        LOG.info('  Creating index file ...')

        Renderer.render_to_directory('index.html', target_dir, add_common_context({
            'languages': sort_by_stars(index_languages),
            'countries': sort_by_stars(index_countries),
            'dt_compiled': compilation_date,
        }))

        LOG.info('Finished.')
