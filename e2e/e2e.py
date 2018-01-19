import argparse
import logging

from selenium import webdriver
from selenium.webdriver.common import keys

logger = logging.getLogger(__name__)


def main(args):
    _configure_logging()

    logger.info('starting remote driver at %s', args.selenium_hub_url)
    driver = webdriver.Remote(
        command_executor=args.selenium_hub_url,
        desired_capabilities={
            'browserName': 'chrome',
            'javascriptEnabled': True
        })
    logger.info('loading app: %s', args.app_url)
    driver.get(args.app_url)

    logger.info('Page Title: [%s]', driver.title)
    driver.save_screenshot('main-page.png')

    logger.info('finding query element')
    elem = driver.find_element_by_id('query')
    elem.send_keys('diet coke')
    elem.send_keys(keys.Keys.RETURN)
    driver.save_screenshot('diet-coke.png')

    elem = driver.find_element_by_id('query')
    elem.send_keys('sushi')
    elem.send_keys(keys.Keys.RETURN)
    driver.save_screenshot('sushi.png')

    driver.close()


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
