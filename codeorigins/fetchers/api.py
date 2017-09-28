from time import time, sleep

import requests

from ..utils import LOG
from .base import Fetcher
from ..common import User, Repository


class Client:
    """Tiny GitHub API client."""

    URL_BASE = 'https://api.github.com/search/'

    def __init__(self, credentials):
        basic_params = {
            'per_page': 100,
        }

        credentials = credentials or (None, None)
        client_id, client_secret = credentials

        if client_id:
            basic_params.update({
                'client_id': client_id,
                'client_secret': client_secret,
            })

        self.basic_params = basic_params

    def iter_users(self, location, language, followers, repos=2):

        yield from self._search('users', {

            'location': location,
            'language': language,
            'followers': '>=%s' % followers,
            'repos': '>=%s' % repos,

        }, sort='followers')

    def iter_repos(self, language, stars, user=None):

        filter_dict = {
            'language': language,
            'stars': '>=%s' % stars,
        }
        if user:
            filter_dict['user'] = user

        yield from self._search('repositories', filter_dict, sort='stars')

    def _request(self, url, params=None):

        response = requests.get(url, params=params)

        links = response.links
        url_next = links.get('next', {'url': None})['url']

        rate_limit, rate_remain, rate_reset = map(int, (
            response.headers['x-ratelimit-limit'],
            response.headers['x-ratelimit-remaining'],
            response.headers['x-ratelimit-reset']))

        if rate_remain == 0:
            # Time to sleep before the next request.
            sleep_time = rate_reset - int(time())

            if sleep_time > 0:
                sleep_time += 1  # Just to be sure...
                LOG.warning('! Time to sleep for %ss ...', sleep_time)
                sleep(sleep_time)

        if response.status_code == 403:
            # This should have been never happen.
            raise Exception(response.json()['message'])

        data = response.json()
        items = data.get('items', [])
        items_total = data.get('total_count', 0)

        for item in items:
            yield items_total, item

        if url_next:
            yield from self._request(url_next)

    def _search(self, what, query, sort):

        params = dict(sort=sort)
        params.update(self.basic_params)

        url = self.URL_BASE + what + '?q=' + '+'.join('%s:%s' % (key, val) for key, val in query.items())

        yield from self._request(url, params=params)


class ApiFetcher(Fetcher):
    """Fetches data from GitHub."""

    name = 'api'

    def __init__(self, client_credentials):
        """
        :param tuple client_credentials: Client ID and secret tuple.
        """
        super().__init__()
        self.client = Client(client_credentials)

    def _gather_repos(self, language_name, min_stars):

        languages = self.client.iter_repos(language_name, min_stars)

        for repo_idx, (total_repos, repo) in enumerate(languages, 1):

            if repo_idx == 1:
                LOG.info('    Total repos: %s', total_repos)

            yield repo['owner']['login'], Repository(
                name=repo['name'],
                url=repo['html_url'],
                description=repo['description'],
                stars=repo['stargazers_count'],
            )

    def _gather_users(self, country_name, language_name, min_followers):

        users = self.client.iter_users(country_name, language_name, min_followers)

        for user_idx, (total_users, user) in enumerate(users, 1):

            if user_idx == 1:
                LOG.info('      Total users in `%s`: %s', country_name, total_users)

            user_login = user['login']

            yield user_login, User(type=user['type'], name=user_login, avatar=user['avatar_url'], repos=[])
