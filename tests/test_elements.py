# -*- coding: utf-8 -*-

"""

test smallparts.markup.elements

"""

import unittest

from smallparts.markup import elements


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_element_attribute(self):
        """Element attributes (underlines are translated)"""
        self.assertEqual(
            elements.XmlElement('abstract').single_attribute(
                'script_environment__', '__main__'),
            ' script-environment="__main__"')
        self.assertEqual(
            elements.XmlElement('x').single_attribute(
                'onClick',
                'return confirm("really?");'),
            """ onClick='return confirm("really?");'""")
        # In HTML, attribute names are lowercased automatically
        self.assertEqual(
            elements.XhtmlStrictElement('p').single_attribute(
                'onClick',
                'return confirm("really?");'),
            """ onclick='return confirm("really?");'""")

    def test_attributes_string(self):
        """XML attributes"""
        self.assertEqual(
            elements.XmlElement('html').attributes_string(
                (('xmlns', 'http://www.w3.org/1999/xhtml'),
                 ('lang', 'en'),
                 ('xml:lang', 'en'))),
            ' xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"')
        self.assertEqual(
            elements.XmlElement('img').attributes_string(
                (('src', 'path/to/image/file'),
                 ('alt_', ''),
                 ('width', 468),
                 ('height', None))),
            ' src="path/to/image/file" alt="" width="468"')
        self.assertEqual(
            elements.XhtmlStrictElement('option').attributes_string(
                (('value', 'option value'),
                 ('SELECTED', True),
                 ('disabled', None))),
            ' value="option value" selected="selected"')

    def test_html_attributes_string(self):
        """HTML attributes"""
        self.assertEqual(
            elements.HtmlElement('option').attributes_string(
                (('value', 'option value'),
                 ('selected', True),
                 ('disabled', None))),
            ' value="option value" selected')
        self.assertEqual(
            elements.HtmlElement('option').attributes_string(
                (('value', 'option value'),
                 ('selected', False))),
            ' value="option value"')

    def test_xml_element(self):
        """XML elements"""
        element_1 = elements.XmlElement('BIG_NAME__')
        element_2 = elements.XmlElement('small_name__')
        self.assertEqual(element_1.tag_name, 'BIG-NAME')
        self.assertEqual(element_2.tag_name, 'small-name')
        self.assertEqual(
            element_2('Multi\n',
                      'Line\n',
                      'Tag content',
                      title='Tag Title'),
            '<small-name title="Tag Title">'
            'Multi\nLine\nTag content</small-name>')
        self.assertEqual(
            element_1(),
            '<BIG-NAME/>')

    def test_xhtml_strict_element(self):
        """XHTML strict elements"""
        self.assertRaises(
            ValueError,
            elements.XhtmlStrictElement,
            'STRIKE')
        element_1 = elements.XhtmlStrictElement('BR_')
        element_2 = elements.XhtmlStrictElement('title__')
        element_3 = elements.XhtmlStrictElement('p__')
        self.assertEqual(element_1.tag_name, 'br')
        self.assertEqual(element_2.tag_name, 'title')
        self.assertEqual(
            element_2('Multi\n',
                      'Line\n',
                      'Tag content',
                      lang='en'),
            '<title lang="en" xml:lang="en">'
            'Multi\nLine\nTag content</title>')
        self.assertEqual(
            element_1(),
            '<br />')
        self.assertEqual(
            element_3('Text paragraph',
                      __class__='special'),
            '<p class="special">Text paragraph</p>')
        self.assertEqual(
            element_3('Another paragraph',
                      __classes__=('one', 'two', 'many')),
            '<p class="many one two">Another paragraph</p>')

    def test_xhtml_transitional_element(self):
        """XHTML transitional elements"""
        element_1 = elements.XhtmlTransitionalElement('BR_')
        element_2 = elements.XhtmlTransitionalElement('strike')
        self.assertEqual(element_1.tag_name, 'br')
        self.assertEqual(element_2.tag_name, 'strike')
        self.assertEqual(
            element_1(),
            '<br />')

    def test_html_element(self):
        """HTML elements"""
        self.assertRaises(
            ValueError,
            elements.HtmlElement,
            'STRIKE')
        element_1 = elements.HtmlElement('BR_')
        element_2 = elements.HtmlElement('title__')
        element_3 = elements.HtmlElement('p__')
        self.assertEqual(element_1.tag_name, 'br')
        self.assertEqual(element_2.tag_name, 'title')
        self.assertEqual(
            element_2('Multi\n',
                      'Line\n',
                      'Tag content',
                      lang='en'),
            '<title lang="en">'
            'Multi\nLine\nTag content</title>')
        self.assertEqual(
            element_1(),
            '<br>')
        self.assertEqual(
            element_3('Text paragraph',
                      __class__='special'),
            '<p class="special">Text paragraph</p>')
        self.assertEqual(
            element_3('Another paragraph',
                      __classes__=('one', 'two', 'many')),
            '<p class="many one two">Another paragraph</p>')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
