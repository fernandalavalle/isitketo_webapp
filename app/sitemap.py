import io
from xml.etree import ElementTree

import food

_BASE_URL = 'https://isitketo.org/'


def get():
    root = ElementTree.Element('urlset')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xsi:schemaLocation',
             ('http://www.sitemaps.org/schemas/sitemap/0.9 '
              'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'))
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    _add_url(root, _BASE_URL)

    for key in _get_food_keys():
        _add_url(root, _BASE_URL + key)

    tree = ElementTree.ElementTree(root)

    with io.BytesIO() as fake_file:
        tree.write(fake_file, encoding='utf-8', xml_declaration=True)
        return fake_file.getvalue()


def _add_url(root, url):
    url_element = ElementTree.SubElement(root, 'url')
    loc = ElementTree.SubElement(url_element, 'loc')
    loc.text = url


def _get_food_keys():
    return sorted([f.key.string_id() for f in food.Food.query().fetch()])
