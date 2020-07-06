# -*- coding: utf-8 -*-

"""

smallparts.text.templates

Enhanced Template class

"""

import re
import string


class EnhancedTemplate(string.Template):

    """string.Template subclass adding one property:
    the list of variable names from the template
    """

    @property
    def variable_names(self):
        """Return the set of variable names in the template"""
        return set(
            ''.join(placeholder)
            for placeholder in re.findall(
                r'(?:{0}({1})|{0}\{{({1})\}})'.format(
                    re.escape(self.delimiter),
                    self.idpattern),
                self.template))


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
