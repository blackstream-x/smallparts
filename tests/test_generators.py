# -*- coding: utf-8 -*-

"""

test smallparts.markup.generators

"""

import unittest

from smallparts.markup import generators


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_css_property(self):
        """CSS property generation"""
        self.assertEqual(
            generators.css_property('width', '320px'),
            'width: 320px;')

    def test_css_important_property(self):
        """CSS '!important' property generation"""
        self.assertEqual(
            generators.css_important_property('color', '#c0c0c0'),
            'color: #c0c0c0 !important;')

    def test_html_document(self):
        """HTML document generation"""
        self.assertEqual(
            generators.html_document(),
            '<!DOCTYPE html>\n'
            '<html lang="en">\n'
            '<head>\n'
            '<meta charset="utf-8">\n'
            '<title>Untitled page</title>\n'
            '</head>\n'
            '<body></body>\n'
            '</html>')
        self.assertEqual(
            generators.html_document(
                head='<meta name="keywords" content="test, unit test">',
                body='<h1>Test page</h1>\n<p>This is a test page</p>\n\n',
                title='Unit test page'),
            '<!DOCTYPE html>\n'
            '<html lang="en">\n'
            '<head>\n'
            '<meta charset="utf-8">\n'
            '<title>Unit test page</title>\n'
            '<meta name="keywords" content="test, unit test">\n'
            '</head>\n'
            '<body>\n'
            '<h1>Test page</h1>\n'
            '<p>This is a test page</p>\n'
            '</body>\n'
            '</html>')
        self.assertEqual(
            generators.html_document(
                dialect=generators.XHTML_1_0_STRICT),
            '<!DOCTYPE html PUBLIC'
            ' "-//W3C//DTD XHTML 1.0 Strict//EN"'
            ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
            '<html xmlns="http://www.w3.org/1999/xhtml"'
            ' lang="en" xml:lang="en">\n'
            '<head>\n'
            '<title>Untitled page</title>\n'
            '</head>\n'
            '<body></body>\n'
            '</html>')
        self.assertRaisesRegex(
            ValueError,
            '^Unsupported HTML dialect',
            generators.html_document,
            dialect='HTML 3.2')
        self.assertRaisesRegex(
            ValueError,
            r'^This function can only generate HTML documents\.$',
            generators.html_document,
            dialect='XML')

    def test_js_function_call(self):
        """Javascript function call generation"""
        self.assertEqual(
            generators.js_function_call(
                'window.setInterval', ('repeat_me()', 300)),
            "window.setInterval('repeat_me()', 300)")

    def test_js_return(self):
        """Javascript return (function call) generation"""
        self.assertEqual(
            generators.js_return(
                'window.setTimeout', 'wait_for_me()', 1500),
            "return window.setTimeout('wait_for_me()', 1500);")

    def test_wrap_cdata(self):
        """Wrap text in a CDATA section"""
        self.assertEqual(
            generators.wrap_cdata('character data'),
            '<![CDATA[character data]]>')
        self.assertEqual(
            generators.wrap_cdata(
                'text with '
                '<![CDATA[already wrapped]]>'
                ' character data'),
            '<![CDATA[text with '
            '<![CDATA[already wrapped]]]]><![CDATA[>'
            ' character data]]>')

    def test_xml_declaration(self):
        """XML declaration"""
        self.assertEqual(
            generators.xml_declaration(),
            '<?xml version="1.0" encoding="utf-8" ?>')
        self.assertEqual(
            generators.xml_declaration(version='1.1', encoding='ascii'),
            '<?xml version="1.1" encoding="ascii" ?>')
        self.assertEqual(
            generators.xml_declaration(standalone=True),
            '<?xml version="1.0" encoding="utf-8" standalone="yes" ?>')
        self.assertEqual(
            generators.xml_declaration(standalone=False),
            '<?xml version="1.0" encoding="utf-8" standalone="no" ?>')

    def test_xml_document(self):
        """XML declaration"""
        self.assertEqual(
            generators.xml_document('<test-element/>'),
            '<?xml version="1.0" encoding="utf-8" ?>\n'
            '<test-element/>')
        self.assertEqual(
            generators.xml_document('<test-element/>',
                                    version='1.1',
                                    standalone=True),
            '<?xml version="1.1" encoding="utf-8" standalone="yes" ?>\n'
            '<test-element/>')

    def test_xml_cache(self):
        """XML elements generation"""
        xml_gen = generators.ElementsCache(generators.XML)
        self.assertEqual(
            xml_gen.outer_element(xml_gen.inner_element(),
                                  attr='value'),
            '<outer-element attr="value"><inner-element/></outer-element>')
        self.assertEqual(
                sorted(xml_gen.__class__._cached_elements[generators.XML]),
                ['inner-element', 'outer-element'])

    def test_html_cache(self):
        """HTML elements generation"""
        html_gen = generators.ElementsCache(generators.HTML_5)
        self.assertEqual(
            html_gen.p__(html_gen.strong('blind text:'),
                         ' lorem ',
                         html_gen.span('ipsum',
                                       style='background: silver;'),
                         __class__='paragraph_style'),
            '<p class="paragraph_style"><strong>blind text:</strong>'
            ' lorem <span style="background: silver;">ipsum</span></p>')
        self.assertEqual(
            repr(html_gen),
            "ElementsCache(dialect='HTML 5')")

    def test_cache_unsupported(self):
        """Unsupported dialect"""
        self.assertRaisesRegex(
            ValueError,
            r'^Unsupported dialect\.$',
            generators.ElementsCache,
            'SGML')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
