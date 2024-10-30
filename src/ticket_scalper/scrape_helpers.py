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
) -> str:
    """return the url in markdown format"""
    logging.debug("link text= %s" % link.text)
    link_url = check_for_relative_links(link.get("href"))
    logging.debug("link href = %s" % link_url)
    return f"- [{link.text}]({link_url})"


def get_urls_from_html(html: str) -> list[str]:
    """given html, return a list of urls"""
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div", class_="search-title")
    logging.debug("found divs: %s" % divs)
    a_tags = []

    for div in divs:
        a_tags.append(div.find("a"))
    logging.debug("found tags: %s" % a_tags)
    return [build_link_markdown(link) for link in a_tags]


def get_urls_from_clipboard() -> None:
    """runs get_urls_from_html using the clipboard contents"""
    html = pyperclip.paste()
    pyperclip.copy("\n".join(get_urls_from_html(html)))
