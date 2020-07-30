# -*- coding: utf-8 -*-

"""

test smallparts.markup.characters

"""

import unittest

from smallparts.markup import characters


class TestSimple(unittest.TestCase):

    """Test the characters module"""

    def test_defuser(self):
        """Defuse text"""
        # Invalid XML version
        self.assertRaisesRegex(
            ValueError,
            '^xml_version must be ',
            characters.Defuser,
            xml_version='2.0')
        # Invalid removals (None)
        self.assertRaisesRegex(
            ValueError,
            '^Please use ',
            characters.Defuser,
            remove=None)
        # Invalid removals (other values)
        self.assertRaisesRegex(
            ValueError,
            '^remove must be ',
            characters.Defuser,
            remove='invalid')
        #
        defuser_default = characters.Defuser()
        defuser_restricted = characters.Defuser(
            remove=characters.REMOVE_RESTRICTED)
        defuser_discouraged = characters.Defuser(
            remove=characters.REMOVE_DISCOURAGED)
        dangerous_text = """\x00 \x80 < & > ' " \ufdd0 lorem ipsum"""
        #
        self.assertEqual(
            defuser_default.defuse(dangerous_text),
            """ \x80 &lt; &amp; &gt; ' " \ufdd0 lorem ipsum""")
        self.assertEqual(
            defuser_restricted.defuse(dangerous_text),
            """  &lt; &amp; &gt; ' " \ufdd0 lorem ipsum""")
        self.assertEqual(
            defuser_discouraged.defuse(dangerous_text),
            """  &lt; &amp; &gt; ' "  lorem ipsum""")
        self.assertEqual(
            characters.Defuser.escape(dangerous_text),
            """\x00 \x80 &lt; &amp; &gt; ' " \ufdd0 lorem ipsum""")

    def test_encode_to_charrefs(self):
        """Encode non-ascii text to charrefs"""
        self.assertEqual(
            characters.encode_to_charrefs('€ äöü'),
            '&#8364; &#228;&#246;&#252;')

    def test_entity(self):
        """Return charref or named entity"""
        self.assertEqual(
            characters.entity(276),
            '&#276;')
        self.assertEqual(
            characters.entity('aacute'),
            '&aacute;')

    def test_charref_from_name(self):
        """Charref from unicode name"""
        self.assertEqual(
            characters.charref_from_name('EURO SIGN'),
            '&#8364;')

    def test_translate_to_charrefs(self):
        """Encode specified characters in source text to charrefs"""
        self.assertEqual(
            characters.translate_to_charrefs('bcd', 'abcdef'),
            'a&#98;&#99;&#100;ef')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
