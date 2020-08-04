# -*- coding: utf-8 -*-

"""

test smallparts.text.transcode

"""

import os.path
import tempfile
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

    def test_to_bytes(self):
        """Encode unicode to bytes"""
        self.assertEqual(
            transcode.to_bytes(
                'Unicode Text with €'),
            b'Unicode Text with \xe2\x82\xac')
        self.assertEqual(
            transcode.to_bytes(
                'Unicode Text with €',
                to_encoding='cp1252'),
            b'Unicode Text with \x80')
        self.assertEqual(
            transcode.to_bytes(
                'Unicode Text with €',
                to_encoding='iso8859-15'),
            b'Unicode Text with \xa4')
        self.assertRaises(
            UnicodeEncodeError,
            transcode.to_bytes,
            'Unicode text with €',
            to_encoding='iso8859-1')
        self.assertRaises(
            TypeError,
            transcode.to_bytes,
            b'UTF-8 text with \xe2\x82\xac')

    def test_anything_to_bytes(self):
        """Safely encode anything to bytes"""
        self.assertEqual(
            transcode.anything_to_bytes(
                'Unicode Text with €'),
            b'Unicode Text with \xe2\x82\xac')
        self.assertEqual(
            transcode.anything_to_bytes(
                b'UTF-8 text with \xe2\x82\xac',
                to_encoding='cp1252'),
            b'UTF-8 text with \x80')
        self.assertEqual(
            transcode.anything_to_bytes(
                23),
            b'23')

    def test_to_utf8(self):
        """Encode unicode to UTF-8"""
        self.assertEqual(
            transcode.to_utf8(
                'Unicode Text with €'),
            b'Unicode Text with \xe2\x82\xac')
        self.assertRaises(
            TypeError,
            transcode.to_utf8,
            b'UTF-8 text with \xe2\x82\xac')

    def test_anything_to_utf8(self):
        """Safely encode anything to UTF-8"""
        self.assertEqual(
            transcode.anything_to_utf8(
                'Unicode Text with €'),
            b'Unicode Text with \xe2\x82\xac')
        self.assertEqual(
            transcode.anything_to_utf8(
                b'UTF-8 text with \xe2\x82\xac'),
            b'UTF-8 text with \xe2\x82\xac')
        self.assertEqual(
            transcode.anything_to_utf8(
                23),
            b'23')

    def test_fix_double_utf8_transformation(self):
        """Fix double UTF-8 transformation"""
        self.assertEqual(
            transcode.fix_double_utf8_transformation(
                'Ã¤Ã¶Ã¼'),
            'äöü')
        self.assertEqual(
            transcode.fix_double_utf8_transformation(
                'â\x82¬',
                wrong_encoding='latin1'),
            '€')
        self.assertRaises(
            ValueError,
            transcode.fix_double_utf8_transformation,
            'Ã¤Ã¶Ã¼',
            wrong_encoding='utf-8')
        # Specifying a wrong wrong_encoding
        # might lead to a UnicodeEncodeError as shown here:
        self.assertRaises(
            UnicodeEncodeError,
            transcode.fix_double_utf8_transformation,
            'â\x82¬',
            wrong_encoding='cp1252')
        # Trying to apply the function to already correct data
        # will raise a UnicodeDecodeError.
        self.assertRaises(
            UnicodeDecodeError,
            transcode.fix_double_utf8_transformation,
            'Ääöüß')

    def test_read_from_file(self):
        """Read text from a file"""
        # transcode.read_from_file()
        with tempfile.TemporaryDirectory() as tmpdirname:
            filename_1 = os.path.join(tmpdirname, 'test_rff_1.txt')
            filename_2 = os.path.join(tmpdirname, 'test_rff_2.txt')
            filename_3 = os.path.join(tmpdirname, 'test_rff_3.txt')
            # CP-1252 autodetect
            with open(filename_1, mode='wb') as file_1:
                file_1.write(b'\xc4\xe4\xf6\xfc\xdf \x80')
            #
            self.assertEqual(
                transcode.read_from_file(filename_1),
                'Ääöüß €')
            # UTF-8 autodetect
            with open(filename_2, mode='wb') as file_2:
                file_2.write(
                    b'\xc3\x84\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x9f \xe2\x82\xac')
            #
            self.assertEqual(
                transcode.read_from_file(filename_2),
                'Ääöüß €')
            # UTF-16 Big endian with BOM autodetect
            with open(filename_3, mode='wb') as file_3:
                # UTF-16 Big endian with BOM
                file_3.write(
                    b'\xfe\xff\x00\xb5\x00 \x00\xa7\x00 \x1e\x9e')
            #
            self.assertEqual(
                transcode.read_from_file(filename_3),
                'µ § ẞ')
        #


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
