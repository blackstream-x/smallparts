# -*- coding: utf-8 -*-

"""

test smallparts.text.transcode

"""

import unittest

from smallparts.text import transcode


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_to_unicode_and_encoding_name(self):
        """Decode bytestrings and also return the encoding name"""
        self.assertEqual(
            transcode.to_unicode_and_encoding_name(
                b'UTF-8 Text with \xe2\x82\xac'),
            ('UTF-8 Text with €', 'utf-8'))
        self.assertEqual(
            transcode.to_unicode_and_encoding_name(
                b'\xef\xbb\xbfUTF-8 Text with \xe2\x82\xac'),
            ('UTF-8 Text with €', 'utf_8_sig'))
        self.assertEqual(
            transcode.to_unicode_and_encoding_name(
                b'UTF-8 Text with \x80'),
            ('UTF-8 Text with €', 'cp1252'))
        self.assertEqual(
            transcode.to_unicode_and_encoding_name(
                b'UTF-8 Text with \xa4',
                from_encoding='iso8859-15'),
            ('UTF-8 Text with €', 'iso8859-15'))
        self.assertRaises(
            UnicodeDecodeError,
            transcode.to_unicode_and_encoding_name,
            b'UTF-8 Text with \xa4',
            from_encoding='utf-8')
        self.assertRaises(
            TypeError,
            transcode.to_unicode_and_encoding_name,
            'Unicode text with €')

    def test_to_unicode(self):
        """Decode bytestrings"""
        self.assertEqual(
            transcode.to_unicode(
                b'UTF-8 Text with \xe2\x82\xac'),
            'UTF-8 Text with €')
        self.assertEqual(
            transcode.to_unicode(
                b'\xef\xbb\xbfUTF-8 Text with \xe2\x82\xac'),
            'UTF-8 Text with €')
        self.assertEqual(
            transcode.to_unicode(
                b'UTF-8 Text with \x80'),
            'UTF-8 Text with €')
        self.assertEqual(
            transcode.to_unicode(
                b'UTF-8 Text with \xa4'),
            'UTF-8 Text with ¤')
        self.assertEqual(
            transcode.to_unicode(
                b'UTF-8 Text with \xa4',
                from_encoding='iso8859-15'),
            'UTF-8 Text with €')

    def test_anything_to_unicode(self):
        """Safely decode bytestrings"""
        self.assertEqual(
            transcode.anything_to_unicode(
                b'UTF-8 Text with \xe2\x82\xac'),
            'UTF-8 Text with €')
        self.assertEqual(
            transcode.anything_to_unicode(
                'UTF-8 Text with €'),
            'UTF-8 Text with €')
        self.assertEqual(
            transcode.anything_to_unicode(
                25),
            '25')
        self.assertEqual(
            transcode.anything_to_unicode(
                ('a', 2, None)),
            "('a', 2, None)")


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
