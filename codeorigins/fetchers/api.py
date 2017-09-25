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

        }, sort=followers)

    def iter_repos(self, user, language, stars):

        yield from self._search('repositories', {

            'language': language,
            'stars': '>=%s' % stars,
            'user': user,

        }, sort='stars')

    def _request(self, url, params=None):

        LOG.debug('Fetching %s ...', url)

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
                LOG.info('  ! Time to sleep for %ss ...', sleep_time)
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

        self.client = Client(client_credentials)

    def _gather(self, country, language, min_stars, min_followers, totals_only=False):

        results = []
        users_seen = []

        users = self.client.iter_users(country, language, min_followers)

        for user_idx, (total_users, user) in enumerate(users, 1):

            if user_idx == 1:

                LOG.info(
                    '> Country: %s. Language: %s. Total users: %s. Min stars: %s',
                    country, language, total_users, min_stars)

                if totals_only:
                    break

            user_login = user['login']

            if user_login in users_seen:
                continue

            users_seen.append(user_login)

            LOG.info('  User (%s/%s): %s ...', user_idx, total_users, user_login)

            repos = []

            for total_repos, repo in self.client.iter_repos(user_login, language, min_stars):
                repo_name = repo['name']

                LOG.debug('    Repository: %s ...', repo_name)

                repos.append(Repository(
                    name=repo_name,
                    url=repo['html_url'],
                    description=repo['description'],
                    stars=repo['stargazers_count'],
                ))

            repos and results.append(User(type=user['type'], name=user_login, avatar=user['avatar_url'], repos=repos))

        return results
