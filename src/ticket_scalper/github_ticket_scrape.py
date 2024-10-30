"""
Fetch the links of the code in from GITHUB stored in the clipboard

This code assumes that you have your GITHUB subdomain applied to GITHUB_URL_ROOT.

To use first copy the section that you would like to pull links from https://github.com/search?q=repo%3Aaiven%2Fmeta-core+updated%3A%3E<FILTER_DATE>+&type=pullrequests

Where <FILTER_DATE> is the -7 days from current
"""

import logging
import os

import dotenv

dotenv.load_dotenv()

GITHUB_URL_ROOT = os.getenv("GITHUB_URL_ROOT", "https://github.com")
logging.info('set GITHUB_URL_ROOT="%s"' % GITHUB_URL_ROOT)

GITHUB_SEARCH_TAG = "div"
GITHUB_SEARCH_ATTR = "class"
GITHUB_ATTR_VALUE = "search-title"
