# -*- coding: utf-8 -*-

"""

test smallparts.markup.elements

"""

import unittest

from smallparts.markup import elements


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_xml_attribute(self):
        """XML attributes (underlines are translated)"""
        self.assertEqual(
            elements.xml_attribute('script_environment__', '__main__'),
            'script-environment="__main__"')
        self.assertEqual(
            elements.xml_attribute('onClick',
                                   'return confirm("really?");'),
            """onClick='return confirm("really?");'""")


# make_attributes_string
# make_html_attributes_string
# XmlElement: .output(), .__call__()
# XhtmlElement: .__call__()
# HtmlElement: .__call__()

# =============================================================================
#     def test_underscores_to_dashes(self):
#         """Text including a trailing newline"""
#         self.assertEqual(
#             translate.underscores_to_dashes('Snake_case_text_example'),
#             'Snake-case-text-example')
#
#     def test_underscores_to_blanks(self):
#         """Text including a trailing newline"""
#         self.assertEqual(
#             translate.underscores_to_blanks('Snake_case_text_example'),
#             'Snake case text example')
# =============================================================================


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
