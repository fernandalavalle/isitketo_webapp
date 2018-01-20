import argparse
import contextlib
import logging

from selenium import webdriver
from selenium.webdriver.common import keys

logger = logging.getLogger(__name__)


def main(args):
    _configure_logging()

    with contextlib.closing(_load_browser(args.selenium_hub_url)) as browser:
        _run_e2e_flow(browser, args.app_url)


def _run_e2e_flow(browser, app_url):
    logger.info('loading app: %s', app_url)
    browser.get(app_url)

    logger.info('Page Title: [%s]', browser.title)
    browser.save_screenshot('main-page.png')

    logger.info('finding query element')
    elem = browser.find_element_by_id('query')
    elem.send_keys('diet coke')
    elem.send_keys(keys.Keys.RETURN)
    browser.save_screenshot('diet-coke.png')

    elem = browser.find_element_by_id('query')
    elem.send_keys('sushi')
    elem.send_keys(keys.Keys.RETURN)
    browser.save_screenshot('sushi.png')


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
                attempts += 1
                continue
            raise


def _configure_logging():
    """Configure the root logger for log output."""
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='IsItKeto E2E Test',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--selenium_hub_url', help='URL for selenium hub', required=True)
    parser.add_argument('--app_url', help='URL for app', required=True)

    main(parser.parse_args())
