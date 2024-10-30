import logging

import click
from bs4 import BeautifulSoup

from .github_ticket_scrape import (
    GITHUB_ATTR_VALUE,
    GITHUB_SEARCH_ATTR,
    GITHUB_SEARCH_TAG,
    GITHUB_URL_ROOT,
)
from .jira_ticket_scrape import (
    JIRA_ATTR_VALUE,
    JIRA_SEARCH_ATTR,
    JIRA_SEARCH_TAG,
    JIRA_URL_ROOT,
)


def check_for_relative_links(
    url: str,
    root_url: str,
) -> str:
    """Append a url if the url found is relative"""

    if not url.startswith("/"):
        return url
    logging.info('Local URL "%s" Detected: adding "%s"' % (url, root_url))
    return f"{root_url}{url}"


def build_link_markdown(
    link,
    link_root: str,
) -> str:
    """return the url in markdown format"""
    logging.debug("link text= %s" % link.text)
    link_url = check_for_relative_links(link.get("href"), link_root)
    logging.debug("link href = %s" % link_url)
    return f"- [{link.text}]({link_url})"


def get_urls_from_html(
    html: str,
    html_search_tag: str,
    soup_attr: str,
    attr_value: str,
    link_root: str,
) -> list[str]:
    """given html, return a list of urls"""
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all(html_search_tag, attrs={soup_attr: attr_value})
    logging.debug("found divs: %s" % tags)
    a_tags = []

    for tag in tags:
        a_tags.append(tag.find("a"))
    logging.debug("found tags: %s" % a_tags)
    return [build_link_markdown(link, link_root) for link in a_tags]


@click.group()
def cli():
    pass


@cli.command()
@click.argument("html")
def github(html: str):
    """github results parser"""
    output = "\n".join(
        get_urls_from_html(
            html,
            GITHUB_SEARCH_TAG,
            GITHUB_SEARCH_ATTR,
            GITHUB_ATTR_VALUE,
            GITHUB_URL_ROOT,
        )
    )

    click.echo(output)


@cli.command()
@click.argument("html")
def jira(html: str):
    output = "\n".join(
        get_urls_from_html(
            html,
            JIRA_SEARCH_TAG,
            JIRA_SEARCH_ATTR,
            JIRA_ATTR_VALUE,
            JIRA_URL_ROOT,
        )
    )

    click.echo(output)
