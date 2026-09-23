import unittest

from extractor.commerce_parser import detect_platform


class CommerceParserTests(unittest.TestCase):
    def test_platform_detection(self):
        cases = {
            "shopify": '<script src="https://cdn.shopify.com/a.js"></script>',
            "woocommerce": '<body class="woocommerce single-product">',
            "shopware": '<meta name="application-name" content="Shopware 6">',
            "magento": '<script>window.mage-cache-storage={}</script>',
            "prestashop": '<meta name="generator" content="PrestaShop">',
            "bigcommerce": '<script src="stencil-utils.min.js"></script>',
            "generic-jsonld": '<script type="application/ld+json">{}</script>',
        }
        for expected, html in cases.items():
            self.assertEqual(detect_platform(html), expected)


if __name__ == "__main__":
    unittest.main()
