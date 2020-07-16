# -*- coding: utf-8 -*-

"""

test smallparts.markup

"""

import unittest

from smallparts import markup


class TestSimple(unittest.TestCase):

    """Test the namespaces module"""

    def test_wrap_cdata(self):
        """Test markup.wrap_cdata"""
        self.assertEqual(
            markup.wrap_cdata('wrapped character data'),
            '<![CDATA[wrapped character data]]>')
        self.assertEqual(
            markup.wrap_cdata('split <![CDATA[*CDATA section*]]> test'),
            '<![CDATA[split <![CDATA[*CDATA section*]]]]><![CDATA[> test]]>')

# =============================================================================
#     def test_namespace(self):
#         """Build a Namespace and test it"""
#         test_object = namespaces.Namespace(roses='red', violets='blue')
#         self.assertEqual(
#             dir(test_object),
#             ['roses', 'violets'])
#         self.assertEqual(
#             repr(test_object),
#             "Namespace({'roses': 'red', 'violets': 'blue'})")
#         self.assertEqual(test_object.roses, 'red')
#         self.assertEqual(test_object.violets, 'blue')
#         self.assertRaises(
#             AttributeError,
#             getattr,
#             test_object,
#             'sugar')
#         del test_object.roses
#         test_object.sugar = 'sweet'
#         self.assertEqual(
#             dir(test_object),
#             ['sugar', 'violets'])
#         self.assertEqual(
#             sorted(test_object.items()),
#             [('sugar', 'sweet'), ('violets', 'blue')])
#
#     def test_default_namespace(self):
#         """Build a DefaultNamespace and test it"""
#         test_object = namespaces.DefaultNamespace(default='product')
#         self.assertEqual(test_object.roses, 'product')
#         self.assertEqual(test_object.violets, 'product')
#         self.assertEqual(
#             sorted(test_object.items()),
#             [('roses', 'product'), ('violets', 'product')])
#         self.assertEqual(test_object.roses, 'product')
#         self.assertEqual(
#             dir(test_object),
#             ['roses', 'violets'])
#
#
#     def test_instant_namespace(self):
#         """Build an InstantNames object and test it"""
#         test_object = namespaces.InstantNames(str.upper)
#         self.assertEqual(test_object.roses, 'ROSES')
#         self.assertEqual(test_object.violets, 'VIOLETS')
#         self.assertEqual(
#             repr(test_object),
#             "InstantNames(<method 'upper' of 'str' objects>,"
#             " roses='ROSES', violets='VIOLETS')")
#         self.assertEqual(
#             test_object.translation_functions,
#             (str.upper, ))
#         self.assertEqual(
#             dir(test_object),
#             ['roses', 'violets'])
# =============================================================================


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
