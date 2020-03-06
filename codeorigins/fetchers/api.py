from time import time, sleep
from itertools import chain

import requests

from ..utils import LOG
from .base import Fetcher
from ..common import User, Repository
from ..settings import REPOS_BASE, STARS_BASE, STARS_MIN


class Client:
    """Tiny GitHub API client."""

    URL_BASE = 'https://api.github.com/search/'

    def __init__(self, credentials):
        common_params = {
            'per_page': 100,
        }

        credentials = credentials or (None, None)
        client_id, client_secret = credentials

        if client_id:
            common_params.update({
                'client_id': client_id,
                'client_secret': client_secret,
            })

        self.common_params = common_params

    def _get_criterion_param(self, floor, ceil):

        if floor != ceil:
            return f'{floor}..{ceil}'

        return f'>={ceil}'

    def iter_users(self, location, language, followers, repos=2):

        yield from self._request({
            'realm': 'users',
            'sort_by': 'followers',
            'narrow_criterion': 'repos',
            'narrow_value_ceil': repos,
            'narrow_value_floor': repos,
            'narrow_value_key': 'repos',
            'query': {
                'location': location,
                'language': language,
                'followers': f'>={followers}',
            },
        })

    def iter_repos(self, language, stars):

        yield from self._request({
            'realm': 'repositories',
            'sort_by': 'stars',
            'narrow_criterion': 'stars',
            'narrow_value_ceil': stars,
            'narrow_value_floor': stars,
            'narrow_value_key': 'stargazers_count',
            'query': {
                'language': language,
            },
        })

    def _request(self, what, limit_bypass_params=None):

        if isinstance(what, str):
            # Simple next page call.
            response = requests.get(what)

        else:
            # New API call or a limit bypass call.
            params = dict(sort=what['sort_by'])
            params.update(self.common_params)

            query = '+'.join(
                f'{key}:{val}' for key, val in list(chain(
                    what['query'].items(),
                    [(what['narrow_criterion'], self._get_criterion_param(
                        what['narrow_value_floor'], what['narrow_value_ceil']
                    ))]
                )))

            limit_bypass_params = what

            if 'items_seen_total' not in what:
                what['items_seen_total'] = 0

            response = requests.get(self.URL_BASE + what['realm'] + '?q=' + query, params=params)

        links = response.links
        url_next = links.get('next', {'url': None})['url']

        rate_limit, rate_remain, rate_reset = map(int, (
            response.headers['x-ratelimit-limit'],
            response.headers['x-ratelimit-remaining'],
            response.headers['x-ratelimit-reset']))

        if rate_remain == 1:
            # Time to sleep before the next request.
            sleep_time = rate_reset - int(time())

            if sleep_time > 0:
                sleep_time += 1  # Just to be sure...
                LOG.warning(f'! Time to sleep for {sleep_time}s ...')
                sleep(sleep_time)

        if response.status_code == 403:
            # This should have been never happen.
            raise Exception(
                f"{response.json()['message']}. "
                f"Rate limit: {rate_limit}. "
                f"Remain: {rate_remain}. "
                f"Reset: {rate_reset}. "
            )

        data = response.json()
        items = data.get('items', [])
        items_total = data.get('total_count', 0)

        if 'items_total' not in limit_bypass_params:
            limit_bypass_params['items_total'] = items_total

        for item in items:
            value = item.get(limit_bypass_params['narrow_value_key'])

            if value:
                limit_bypass_params['narrow_value_ceil'] = value

            limit_bypass_params['items_seen_total'] += 1

            yield items_total, item

        if url_next:
            # More pages.
            LOG.debug('    Trying to get results from the next API page ...')
            yield from self._request(url_next, limit_bypass_params=limit_bypass_params)

        elif limit_bypass_params['items_seen_total'] < limit_bypass_params['items_total']:
            # Bypass API limit.

            LOG.info(
                f"      {limit_bypass_params['items_total'] - limit_bypass_params['items_seen_total']} "
                "items to be processed yet ...",)

            yield from self._request(limit_bypass_params)


class ApiFetcher(Fetcher):
    """Fetches data from GitHub."""

    name = 'api'

    def __init__(self, client_credentials):
        """
        :param tuple client_credentials: Client ID and secret tuple.
        """
        super().__init__()
        self.client = Client(client_credentials)

    def _adjust_min_stars(self, language_name):

        stars_step = 4

        increasing = False
        decreasing = False

        def get_totals(totals, stars):
            nonlocal increasing, decreasing

            for total_repos, _ in self.client.iter_repos(language_name, stars):
                totals = total_repos
                break

            if totals > REPOS_BASE and not decreasing:
                LOG.debug(f'  Too many repos `{totals}`. Adding stars ...')
                increasing = True
                stars_next = stars + stars_step

                if stars_next <= STARS_MIN:
                    return totals, STARS_MIN

                totals, stars = get_totals(totals, stars_next)

            elif totals < REPOS_BASE and not increasing:
                LOG.debug(f'  Too few repos `{totals}`. Removing stars ...')
                decreasing = True
                stars_next = stars - stars_step

                if stars_next <= STARS_MIN:
                    return totals, STARS_MIN

                totals, stars = get_totals(totals, stars_next)

            return totals, stars

        _, min_stars = get_totals(0, STARS_BASE)

        return min_stars

    def _gather_repos(self, language_name, min_stars):

        languages = self.client.iter_repos(language_name, min_stars)

        for repo_idx, (total_repos, repo) in enumerate(languages, 1):

            if repo_idx == 1:
                LOG.info(f'    Total repos: {total_repos}')

            yield repo['owner']['login'], Repository(
                name=repo['name'],
                url=repo['html_url'],
                description=repo['description'],
                stars=repo['stargazers_count'],
                language=repo['language'],
            )

    def _gather_users(self, country_name, language_name, min_followers):

        users = self.client.iter_users(country_name, language_name, min_followers)

        for user_idx, (total_users, user) in enumerate(users, 1):

            if user_idx == 1:
                LOG.info(f'      Total users in `{country_name}`: {total_users}')

            user_login = user['login']

            yield user_login, User(type=user['type'], name=user_login, avatar=user['avatar_url'], repos=[])
