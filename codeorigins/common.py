from collections import namedtuple


Repository = namedtuple('Repository', ['name', 'url', 'description', 'stars', 'language'])
User = namedtuple('User', ['type', 'name', 'avatar', 'repos'])
