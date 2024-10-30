"""
Fetch the links of the code in from JIRA stored in the clipboard

This code assumes that you have your JIRA subdomain applied to JIRA_URL_ROOT.

To use first copy the section that you would like to pull links from 
"""

import logging
import os

import dotenv

dotenv.load_dotenv()

JIRA_URL_ROOT = os.getenv("JIRA_URL_ROOT", "")
logging.info('set JIRA_URL_ROOT="%s"' % JIRA_URL_ROOT)
JIRA_SEARCH_TAG = "ul"
JIRA_SEARCH_ATTR = "aria-label"
JIRA_ATTR_VALUE = "Issues"
