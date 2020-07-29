# -*- coding: utf-8 -*-

"""

test smallparts.markup.parsers

"""

import unittest

from html import entities

from smallparts.markup import parsers


class TestSimple(unittest.TestCase):

    """Test the parsers module"""

    def test_entity_resolver(self):
        """Resolve entities"""
        source_text = '&lt; &amp; &gt; &ouml; &aacute;' \
            ' &#x20ac; &#177; &special;'
        # Default: XML named entities only
        xml_resolver = parsers.EntityResolver()
        self.assertEqual(
            xml_resolver.resolve_all_entities(source_text),
            '< & > &ouml; &aacute; € ± &special;')
        # Named entities from a dict (HTML entities from html.entities)
        html_resolver = parsers.EntityResolver(entities.name2codepoint)
        self.assertEqual(
            html_resolver.resolve_all_entities(source_text),
            '< & > ö á € ± &special;')
        # Named entities from a dict (special values)
        special_resolver = parsers.EntityResolver(
            {'special': 'Extraordinary Value'})
        self.assertEqual(
            special_resolver.resolve_all_entities(source_text),
            '&lt; &amp; &gt; &ouml; &aacute;'
            ' € ± Extraordinary Value')
        #
        # Invalid code points
        self.assertRaises(
            ValueError,
            parsers.EntityResolver,
            {'toobig': 0x110000})
        self.assertRaises(
            ValueError,
            parsers.EntityResolver,
            {'negative': -1})
        # Non-string and non-integer replacements
        self.assertRaises(
            ValueError,
            parsers.EntityResolver,
            {'unusable': ['list', 'of', 4, 'items']})

    def test_tag_stripper(self):
        """Strip HTML tags"""
        html_document = (
            '<!DOCTYPE html>\n'
            '<html>\n'
            '<body>\n'
            '<h2>HTML Images</h2>\n'
            '<p>HTML images are defined with the img tag:</p>\n'
            '<IMG src="w3schools.jpg" alt="W3Schools.com"'
            ' width="104" height="142"> <img src="logo.png">\n'
            '</body>\n'
            '</html>')
        tag_stripper = parsers.HtmlTagStripper()
        tag_stripper.feed(html_document)
        self.assertEqual(
            tag_stripper.content,
            'HTML Images\n'
            'HTML images are defined with the img tag:\n'
            '[image: W3Schools.com]')
        self.assertDictEqual(
            tag_stripper.images[0],
            dict(src="w3schools.jpg",
                 alt="W3Schools.com",
                 width="104",
                 height="142"))
        self.assertDictEqual(
            tag_stripper.images[1],
            dict(src="logo.png"))
        tag_stripper_2 = parsers.HtmlTagStripper(image_placeholders='always')
        tag_stripper_2.feed(html_document)
        self.assertEqual(
            tag_stripper_2.content,
            'HTML Images\n'
            'HTML images are defined with the img tag:\n'
            '[image: W3Schools.com] [image]')
        tag_stripper_3 = parsers.HtmlTagStripper(image_placeholders='never')
        tag_stripper_3.feed(html_document)
        self.assertEqual(
            tag_stripper_3.content,
            'HTML Images\n'
            'HTML images are defined with the img tag:')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
