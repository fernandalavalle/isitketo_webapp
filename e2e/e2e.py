import argparse
import contextlib
import logging
import time

from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import ui

logger = logging.getLogger(__name__)


class Error(Exception):
    pass


class UnexpectedValueError(Error):
    pass


def main(args):
    _configure_logging()
    for browser_name in ('chrome', 'firefox'):
        with contextlib.closing(
                _load_browser(browser_name, args.selenium_hub_url)) as browser:
            TestFlow(browser, args.app_url).start()


def _configure_logging():
    """Configure the root logger for log output."""
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


def _load_browser(browser_name, selenium_hub_url):
    logger.info('loading remote webdriver: %s at %s', browser_name,
                selenium_hub_url)
    attempts = 0
    MAX_ATTEMPTS = 10
    while True:
        try:
            return webdriver.Remote(
                command_executor=selenium_hub_url,
                desired_capabilities={
                    'browserName': browser_name,
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
        try:
            self._do_flow()
        except:
            self._dump_debug()
            raise

    def _do_flow(self):
        self._load_homepage()

        self._search('diet coke')
        self._verify_meta_property('og:title', u'Diet Coke - Is It Keto?')
        self._verify_meta_property(
            'og:image',
            u'https://storage.googleapis.com/isitketo/isitketo-meter-5-square-600w.png'
        )
        self._verify_meta_property('og:url', u'https://isitketo.org/diet-coke')

        self._search('sushi')
        self._verify_meta_property('og:title', u'Sushi - Is It Keto?')
        self._verify_meta_property(
            'og:image',
            u'https://storage.googleapis.com/isitketo/isitketo-meter-2-square-600w.png'
        )
        self._verify_meta_property('og:url', u'https://isitketo.org/sushi')

    def _load_homepage(self):
        logger.info('loading app: %s', self._app_url)
        self._browser.get(self._app_url)

    def _search(self, query):
        logger.info('searching for [%s]', query)
        search_input = self._browser.find_element_by_id('query')
        search_input.send_keys(query)
        search_input.send_keys(keys.Keys.RETURN)

    def _verify_meta_property(self, property_name, expected_value):
        xpath = '//meta[@property="%s"]' % property_name
        self._wait_for_element(xpath)
        element = self._browser.find_element_by_xpath(xpath)
        actual_value = element.get_attribute('content')
        if expected_value != actual_value:
            raise UnexpectedValueError(
                'Unexpected value for %s. Want %s, got %s', property_name,
                expected_value, actual_value)

    def _wait_for_element(self, xpath):
        element_present = expected_conditions.presence_of_element_located(
            (by.By.XPATH, xpath))
        ui.WebDriverWait(self._browser, timeout=5).until(element_present)

    def _dump_debug(self):
        self._browser.save_screenshot('screenshot.png')
        logging.warning(self._browser.page_source)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='IsItKeto E2E Test',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--selenium_hub_url', help='URL for selenium hub', required=True)
    parser.add_argument('--app_url', help='URL for app', required=True)

    main(parser.parse_args())
