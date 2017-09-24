from .api import ApiFetcher
from ..utils import sortdict


FETCHERS = sortdict({fetcher.name: fetcher for fetcher in [ApiFetcher]})
"""Available data fetchers."""
