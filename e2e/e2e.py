import argparse
import contextlib
import logging
import time

from selenium import webdriver
from selenium.webdriver.common import keys

logger = logging.getLogger(__name__)


def main(args):
    _configure_logging()

    with contextlib.closing(_load_browser(args.selenium_hub_url)) as browser:
        TestFlow(browser, args.app_url).start()


def _configure_logging():
    """Configure the root logger for log output."""
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


def _load_browser(selenium_hub_url):
    logger.info('loading remote webdriver at %s', selenium_hub_url)
    attempts = 0
    MAX_ATTEMPTS = 10
    while True:
        try:
            return webdriver.Remote(
                command_executor=selenium_hub_url,
                desired_capabilities={
                    'browserName': 'chrome',
                    'javascriptEnabled': True
                })
        except Exception as e:
            if attempts < MAX_ATTEMPTS:
                logging.warning('Failed to connect to webdriver: %s', e.message)
                attempts += 1
                time.sleep(2)
                continue
            raise


class TestFlow(object):

    def __init__(self, browser, app_url):
        self._browser = browser
        self._app_url = app_url

    def start(self):
        self._load_homepage()
        self._search('diet coke')
        self._search('sushi')

    def _load_homepage(self):
        logger.info('loading app: %s', self._app_url)
        self._browser.get(self._app_url)

    def _search(self, query):
        logger.info('searching for [%s]', query)
        search_input = self._browser.find_element_by_id('query')
        search_input.send_keys(query)
        search_input.send_keys(keys.Keys.RETURN)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='IsItKeto E2E Test',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--selenium_hub_url', help='URL for selenium hub', required=True)
    parser.add_argument('--app_url', help='URL for app', required=True)

    main(parser.parse_args())
