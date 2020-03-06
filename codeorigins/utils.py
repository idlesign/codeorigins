import json
import logging
import os
from collections import OrderedDict, defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
from operator import attrgetter
from os import makedirs, path, getcwd, chdir
from time import time

import jinja2

LOG = logging.getLogger('codeorigins')


def get_datetime_string():
    """Returns string with current date and time.

    :rtype: str
    """
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')


def configure_logging(level=logging.INFO):
    """Configures logging.

    :param level: Log level.

    """
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')


def get_local_dump_dir():
    """Returns dump directory from sources.

    :rtype: str
    """
    return path.join(path.dirname(__file__), 'dump')


def sortdict(d):
    """Returns ordered dict sorting input dict by keys."""
    return OrderedDict(((item[0], item[1]) for item in sorted(d.items(), key=lambda item: item[0])))


class Dump:
    """Dumping and undumping related functions."""

    @classmethod
    def write(cls, data, dump_dir=None):
        """Dumps data.

        :param dict data:

        :param str dump_dir: Target directory to put dumps into.

        """
        dump_dir = dump_dir or get_local_dump_dir()

        for country, languages in data.items():
            for language, users in languages.items():

                if not users:
                    continue

                filepath = f'{dump_dir}/{country.lower()}_{language.lower()}.json'
                makedirs(path.dirname(filepath), exist_ok=True)

                with open(filepath, 'w') as f:
                    json.dump(users, f)

    @classmethod
    def read(cls, dump_dir=None):
        """Reads dumps and returns a dictionary with data from it.

        Dictionary sample:
            {
                'ru: {
                    'python': [
                        User,
                        ...
                    ]
                },
                ...
            }

        :param str dump_dir: If not set dump dir from sources is used.

        :rtype: dict

        """
        from .common import User, Repository

        dump_dir = dump_dir or get_local_dump_dir()
        join = os.path.join
        basename = os.path.basename
        splitext = os.path.splitext

        def get_dir_items(target_dir, func_check):

            items = []

            for sub in sorted(os.listdir(target_dir)):
                sub_path = join(target_dir, sub)

                func_check(sub_path) and items.append(sub_path)

            return items

        stars_getter = attrgetter('stars')

        results = defaultdict(dict)

        for dump_fpath in get_dir_items(dump_dir, os.path.isfile):
            name, ext = splitext(basename(dump_fpath))

            if ext != '.json':
                continue

            country, _, language = name.partition('_')

            with open(dump_fpath) as f:
                language_data = json.load(f)

            users = []

            for user_data in language_data['users']:

                user = User(*user_data)
                user = user._replace(
                    repos=sorted(
                        list(map(lambda repo: Repository(*repo), user.repos)),
                        key=stars_getter, reverse=True))

                users.append(user)

            language_data['users'] = users

            results[language][country] = language_data

        return results


@contextmanager
def logtime(title):
    """Context manager logging elapsed time."""
    started = time()

    LOG.info(f'{title} ...')

    yield

    LOG.info(f'{title} took {round(int(time() - started) / 60, 1)}m')


class Renderer:
    """Encapsulates template rendering related functions."""

    @classmethod
    def render_template(cls, filename, context):
        """Renders contents from the given template.

        :param str filename:
        :param dict context:
        :rtype: str

        """
        old_dir = getcwd()
        chdir(path.dirname(__file__))

        try:
            template_path = path.abspath('templates/')

            env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
            rendered = env.get_template(filename).render(**context)

        finally:
            chdir(old_dir)

        return rendered

    @classmethod
    def render_to_directory(cls, template, target_dir, context, target_filename=None):
        """Renders template and saves contents into file in the given directory.

        :param str template:
        :param str target_dir:
        :param dict context:
        :param str target_filename:

        """
        contents = cls.render_template(template, context)

        target_fpath = os.path.join(target_dir, target_filename or template)

        with open(target_fpath, 'w') as f:
            f.write(contents)
