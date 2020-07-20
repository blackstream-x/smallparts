# -*- coding: utf-8 -*-

"""

smallparts.text.templates

Enhanced String Template class

"""

import string


class EnhancedStringTemplate(string.Template):

    """string.Template subclass adding one property:
    the set of variable names from the template
    """

    @property
    def variable_names(self):
        """Return the set of variable names in the template"""
        result = set()
        # pylint: disable=no-member ; false positive on Template.pattern
        for placeholder_match in self.pattern.finditer(self.template):
            placeholder_name = placeholder_match.group('named') or \
                placeholder_match.group('braced')
            if placeholder_name:
                result.add(placeholder_name)
            #
        #
        return result


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
