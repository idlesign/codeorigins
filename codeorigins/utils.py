import json
import logging
from collections import OrderedDict
from contextlib import contextmanager
from datetime import datetime
from os import makedirs, path
from time import time

LOG = logging.getLogger('codeorigins')

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def sortdict(d):
    """Returns ordered dict sorting input dict by keys."""
    return OrderedDict(((item[0], item[1]) for item in sorted(d.items(), key=lambda item: item[0])))


def dump(data, dump_dir=None):
    """Dumps data.

    :param dict data:

    :param str dump_dir: Target directory to put dumps into.

    """
    dump_dir = dump_dir or 'dumps'

    date = datetime.now().strftime('%Y%m%d%H%M')

    for country, languages in data.items():
        for language, users in languages.items():
            if not users:
                continue

            filepath = '%s/%s/%s_%s.json' % (dump_dir, date, country.lower(), language.lower())
            makedirs(path.dirname(filepath), exist_ok=True)

            with open(filepath, 'w') as f:
                json.dump(users, f)


@contextmanager
def logtime(title):
    """Context manager logging elapsed time."""
    started = time()

    yield

    LOG.info('%s took %sm', title, round(int(time() - started) / 60, 1))
