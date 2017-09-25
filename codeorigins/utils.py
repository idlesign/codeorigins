import json
import logging
import os
from collections import OrderedDict, defaultdict
from contextlib import contextmanager
from operator import attrgetter
from os import makedirs, path, getcwd, chdir
from time import time

import jinja2


LOG = logging.getLogger('codeorigins')

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


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

                filepath = '%s/%s_%s.json' % (dump_dir, country.lower(), language.lower())
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

        results = defaultdict(lambda: defaultdict(list))

        for dump_fpath in get_dir_items(dump_dir, os.path.isfile):
            name, ext = splitext(basename(dump_fpath))

            if ext != '.json':
                continue

            country, _, language = name.partition('_')

            with open(dump_fpath) as f:
                data = json.load(f)

            for user_data in data:

                user = User(*user_data)
                user = user._replace(
                    repos=sorted(
                        list(map(lambda repo: Repository(*repo), user.repos)),
                        key=stars_getter, reverse=True))

                results[language][country].append(user)

        return results


@contextmanager
def logtime(title):
    """Context manager logging elapsed time."""
    started = time()

    yield

    LOG.info('%s took %sm', title, round(int(time() - started) / 60, 1))


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
