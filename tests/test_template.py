# -*- coding: utf-8 -*-

"""

test smallparts.text.templates

"""

import unittest

from smallparts.text import templates


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_variable_names(self):
        """Variable names from the templaet string"""
        tmpl = templates.EnhancedStringTemplate(
            '${salutation} $customer,\n\n'
            'your order (${order_data}) has been placed and'
            ' will be delivered at ${delivery_date}.')
        self.assertEqual(
            tmpl.variable_names,
            {'customer', 'delivery_date', 'order_data', 'salutation'})


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
