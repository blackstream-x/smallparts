# -*- coding: utf-8 -*-

"""

test smallparts.namespces

"""

import unittest

from smallparts import namespaces


class TestSimple(unittest.TestCase):

    """Test the namespaces module"""

    def test_namespace(self):
        """Build a Namespace and test it"""
        test_object = namespaces.Namespace(roses='red', violets='blue')
        self.assertEqual(
            dir(test_object),
            ['roses', 'violets'])
        self.assertEqual(
            repr(test_object),
            "Namespace({'roses': 'red', 'violets': 'blue'})")
        self.assertEqual(test_object.roses, 'red')
        self.assertEqual(test_object.violets, 'blue')
        self.assertRaises(
            AttributeError,
            getattr,
            test_object,
            'sugar')
        del test_object.roses
        test_object.sugar = 'sweet'
        self.assertEqual(
            dir(test_object),
            ['sugar', 'violets'])
        self.assertEqual(
            sorted(test_object.items()),
            [('sugar', 'sweet'), ('violets', 'blue')])

    def test_default_namespace(self):
        """Build a DefaultNamespace and test it"""
        test_object = namespaces.DefaultNamespace(default='product')
        self.assertEqual(test_object.roses, 'product')
        self.assertEqual(test_object.violets, 'product')
        self.assertEqual(
            sorted(test_object.items()),
            [('roses', 'product'), ('violets', 'product')])
        self.assertEqual(test_object.roses, 'product')
        self.assertEqual(
            dir(test_object),
            ['roses', 'violets'])

    def test_enhanced_namespace(self):
        """Build an EnhancedNamespace and test it"""
        simple = namespaces.Namespace(roses='red',
                                      violets='blue',
                                      sugar='sweet')
        enhanced_1 = namespaces.EnhancedNamespace.from_object(
            simple)
        self.assertEqual(
            sorted(enhanced_1.items()),
            [('roses', 'red'), ('sugar', 'sweet'), ('violets', 'blue')])
        enhanced_2 = namespaces.EnhancedNamespace.from_object(
            simple, names=('roses', 'violets'))
        self.assertEqual(
            sorted(enhanced_2.items()),
            [('roses', 'red'), ('violets', 'blue')])
        enhanced_3 = namespaces.EnhancedNamespace.from_mapping(
            {'a': 1, 'b': 3, 'x': 27}, names=('x', 'a'))
        self.assertEqual(
            sorted(enhanced_3.items()),
            [('a', 1), ('x', 27)])
        enhanced_4 = namespaces.EnhancedNamespace.from_mapping(
            {'a': 1, 'b': 3, 'x': 27})
        self.assertEqual(
            sorted(enhanced_4.items()),
            [('a', 1), ('b', 3), ('x', 27)])
        enhanced_5 = namespaces.EnhancedNamespace.from_sequence(
            [('abc', 'xxx'), ('def', 'yyy'), ('ghi', 222), ('jkl', None)],
            names=('def', 'jkl'))
        self.assertEqual(
            sorted(enhanced_5.items()),
            [('def', 'yyy'), ('jkl', None)])
        enhanced_6 = namespaces.EnhancedNamespace.from_sequence(
            [('abc', 'xxx'), ('def', 'yyy'), ('ghi', 222), ('jkl', None)])
        self.assertEqual(
            sorted(enhanced_6.items()),
            [('abc', 'xxx'), ('def', 'yyy'), ('ghi', 222), ('jkl', None)])

    def test_instant_namespace(self):
        """Build an InstantNames object and test it"""
        test_object = namespaces.InstantNames(str.upper)
        self.assertEqual(test_object.roses, 'ROSES')
        self.assertEqual(test_object.violets, 'VIOLETS')
        self.assertEqual(
            repr(test_object),
            "InstantNames(<method 'upper' of 'str' objects>,"
            " roses='ROSES', violets='VIOLETS')")
        self.assertEqual(
            test_object.translation_functions,
            (str.upper, ))
        self.assertEqual(
            dir(test_object),
            ['roses', 'violets'])


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
