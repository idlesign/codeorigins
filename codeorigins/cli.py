import click

from codeorigins import VERSION
from codeorigins.utils import Dump
from codeorigins.composer import HtmlComposer
from codeorigins.fetchers import FETCHERS
from codeorigins.settings import COUNTRIES, LANGUAGES


if False:  # pragma: nocover
    from codeorigins.fetchers.base import Fetcher


def fetcher_dump(fetcher_alias, credentials, into, country, language, totals_only):
    fetcher = FETCHERS[fetcher_alias](credentials)  # type: Fetcher

    results = fetcher.run(
        languages=[language] if language else None,
        countries=[country] if country else None,
        totals_only=totals_only)

    Dump.write(results, dump_dir=into)


@click.group()
@click.version_option(version='.'.join(map(str, VERSION)))
def base():
    """codeorigins command line utility."""


@base.group()
@click.option(
    '--into', help='Directory to store dumps into.', type=click.Path(exists=True, file_okay=False))
@click.option('--country', help='Country to dump.', type=click.Choice(COUNTRIES.keys()))
@click.option('--language', help='Language to dump.', type=click.Choice(LANGUAGES.keys()))
@click.option('--totals_only', help='Don\'t fetch stats. Only log total users.', is_flag=True)
@click.pass_context
def dump(ctx, into, country, language, totals_only):
    """Dumps statistics from GitHub using the given fetcher."""
    ctx.obj['into'] = into
    ctx.obj['country'] = country
    ctx.obj['language'] = language
    ctx.obj['totals_only'] = totals_only


@base.command()
@click.option(
    '--dump_dir', help='Directory to read dump from.', type=click.Path(exists=True, file_okay=False))
@click.option(
    '--html_dir', help='Directory to store HTML into. Current working dir if not set.',
    type=click.Path(exists=True, file_okay=False))
def make_html(dump_dir, html_dir):
    data = Dump.read(dump_dir)
    HtmlComposer(data).make_html(html_dir)


@dump.command()
@click.option('--credentials', help='GitHub client credentials: <client_id>,<client_secret>')
@click.pass_context
def api(ctx, credentials):
    """Fetch stats using API methods."""

    credentials = credentials.split(',', 1) if credentials else (None, None)
    ctx = ctx.obj
    fetcher_dump(
        'api', credentials, ctx['into'],
        ctx['country'], ctx['language'],
        totals_only=ctx['totals_only'])


@base.command()
def show_settings():
    """Prints out basic settings."""

    click.secho('Countries:', fg='green')
    click.secho(', '.join(COUNTRIES.keys()))

    click.secho('Languages:', fg='green')
    click.secho(', '.join(LANGUAGES.keys()))


def main():
    """
    CLI entry point.
    """
    base(obj={})


if __name__ == '__main__':
    main()
