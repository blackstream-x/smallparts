# -*- coding: utf-8 -*-

"""

smallparts.namespaces - simple dict-based namespaces

------------------------------------------------------------------------

Adapted from:

ActiveState Code » Recipes » A Simple Namespace Class (Python recipe)
<http://code.activestate.com/recipes/577887-a-simple-namespace-class/>

------------------------------------------------------------------------

"""


#
# Classes
#


class Namespace(dict):

    """A dict subclass that exposes its items as attributes.

    Warning: Namespace instances only have direct access to the
    attributes defined in the visible_attributes tuple
    """

    visible_attributes = ('items', )

    def __repr__(self):
        """Object representation"""
        return '{0}({1})'.format(
            type(self).__name__,
            super(Namespace, self).__repr__())

    def __dir__(self):
        """Members sequence"""
        return tuple(self)

    def __getattribute__(self, name):
        """Access a visible attribute
        or return an existing dict member
        """
        if name in type(self).visible_attributes:
            return object.__getattribute__(self, name)
        #
        try:
            return self[name]
        except KeyError:
            raise AttributeError(
                '{0!r} object has no attribute {1!r}'.format(
                    type(self).__name__, name))
        #

    def __setattr__(self, name, value):
        """Set an attribute"""
        self[name] = value

    def __delattr__(self, name):
        """Delete an attribute"""
        del self[name]


class DefaultNamespace(Namespace):

    """Namespace object with a default value for non-existent
    attributes
    """

    visible_attributes = ('items', 'default__value__')

    def __init__(self, *args, **kwargs):
        """Initialize like a dict, but steal the 'default'
        keyword argument if given"""
        object.__setattr__(self,
                           'default__value__',
                           kwargs.pop('default', None))
        super(DefaultNamespace, self).__init__(*args, **kwargs)

    def __getattribute__(self, name):
        """Access a visible attribute
        or return the default value (and cache it)
        """
        if name in type(self).visible_attributes:
            return object.__getattribute__(self, name)
        #
        return dict.setdefault(self, name, self.default__value__)


class EnhancedNamespace(Namespace):

    """Namespace object with additional constructor methods
    for using only selected names
    """

    @classmethod
    def from_object(cls, object_, names=None):
        """Try to construct a Namespace object from an arbitrary object"""
        if names is None:
            names = dir(object_)
        #
        return cls((name, getattr(object_, name)) for name in names)

    @classmethod
    def from_mapping(cls, mapping, names=None):
        """Construct a Namespace object from a mapping (i.e a dict)"""
        if names:
            return cls((name, mapping[name]) for name in names)
        #
        return cls(mapping)

    @classmethod
    def from_sequence(cls, sequence, names=None):
        """Construct a Namespace object from a sequence of 2-tuples"""
        if names:
            return cls((name, value) for (name, value) in sequence
                       if name in names)
        #
        return cls(sequence)


class InstantNames(dict):

    """Namespace object where instance attributes are defined
    on access, derived from the given name with the translation
    functions applied on it
    """

    translations = 'translation_functions'

    def __init__(self, *translation_functions, **set_values_directly):
        """Register translation functions
        and set the given values directly
        """
        self.translation_functions = translation_functions
        super(InstantNames, self).__init__(set_values_directly)

    def __dir__(self):
        """Members sequence"""
        return tuple(self)

    def __repr__(self):
        """Object representation"""
        instance_attributes_list = [
            repr(function) for function
            in object.__getattribute__(self, type(self).translations)]
        instance_attributes_list.extend(
            '{0}={1!r}'.format(name, self[name]) for name in self)
        return '{0}({1})'.format(
            type(self).__name__,
            ', '.join(instance_attributes_list))

    def __getattribute__(self, name):
        """Access an allowed internal attribute
        or set the instance attribute
        """
        if name in (type(self).translations,):
            return object.__getattribute__(self, name)
        #
        try:
            attribute_value = self[name]
        except KeyError:
            attribute_value = name
            for translation in object.__getattribute__(
                    self, type(self).translations):
                attribute_value = translation(attribute_value)
            self[name] = attribute_value
        return attribute_value


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
