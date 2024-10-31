"""the ticket scalper CLI implementation"""

import logging
import pyperclip
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


def _check_for_relative_links(
    url: str,
    root_url: str,
) -> str:
    """Append a url if the url found is relative"""

    if not url.startswith("/"):
        return url
    logging.info('Local URL "%s" Detected: adding "%s"' % (url, root_url))
    return f"{root_url}{url}"


def _build_link_markdown(
    link,
    link_root: str,
) -> str:
    """return the url in markdown format"""
    logging.debug("link text= %s" % link.text)
    link_url = _check_for_relative_links(link.get("href"), link_root)
    logging.debug("link href = %s" % link_url)
    return f"- [{link.text}]({link_url})"


def _get_urls_from_html(
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
    return [_build_link_markdown(link, link_root) for link in a_tags]


@click.command()
@click.argument(
    "parser",
    type=click.Choice(["jira", "github"]),
)
@click.argument("html", required=False)
@click.option("--clipboard/--no-clipboard", default=False)
def cli(parser, clipboard: bool, html: str | None = None):
    """parse the contents of search results and return markdown links"""
    if clipboard:
        html = pyperclip.paste()

    if not html:
        raise ValueError(
            "No HTML Detected. Please provide an HTML value or add the --clipboard option"
        )

    match parser:
        case "github":
            output = "\n".join(
                _get_urls_from_html(
                    html,
                    GITHUB_SEARCH_TAG,
                    GITHUB_SEARCH_ATTR,
                    GITHUB_ATTR_VALUE,
                    GITHUB_URL_ROOT,
                )
            )

        case "jira":
            output = "\n".join(
                _get_urls_from_html(
                    html,
                    JIRA_SEARCH_TAG,
                    JIRA_SEARCH_ATTR,
                    JIRA_ATTR_VALUE,
                    JIRA_URL_ROOT,
                )
            )
        case _:
            raise ValueError("Invalid Option")

    click.echo(output)
