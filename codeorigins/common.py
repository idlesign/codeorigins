from collections import namedtuple


Repository = namedtuple('Repository', ['name', 'url', 'description', 'stars'])
User = namedtuple('User', ['type', 'name', 'avatar', 'repos'])
