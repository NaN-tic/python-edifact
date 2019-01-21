# encoding: utf8
##############################################################################
#
#    Copyright (C) 2011-2019 NaN Projectes de Programari Lliure, S.L.
#                            http://www.NaN-tic.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from __future__ import absolute_import
from copy import copy
from builtins import object


class Characters(object):
    u"""A set of control characters to use."""

    def __init__(self):
        # The control character used to separate components.
        self.component_separator = u':'

        # The control character used to separate data elements.
        self.data_separator = u'+'

        # The control character used as a decimal point.
        self.decimal_point = u','

        # The control character used as an escape character.
        self.escape_character = u'?'

        # Reserved for future use
        self.reserved_character = u' '

        # The control character used as an segment terminator.
        self.segment_terminator = u"'"

    @classmethod
    def from_str(cls, string):
        u"""Returns a new instance with control characters set to given string.
        :param string: The string to set the control characters to
        """
        if string[0:3] == u'UNA':
            string = string[3:9]
        assert len(string) >= 6

        characters = cls()
        characters.component_separator = string[0]
        characters.data_separator = string[1]
        characters.decimal_point = string[2]
        characters.escape_character = string[3]
        characters.reserved_character = string[4]
        characters.segment_terminator = string[5]
        return characters

    def with_control_character(self, cc_type, char):
        u"""Set a control character.

        :param cc_type: The type of control character to set,
            as one of the following attribute strings:
            componentSeparator, dataSeparator, decimalPoint,
            escapeCharacter, segmentTerminator
        :param char: The character to set it to
        :return: clone of self
        """
        if len(char) != 1:
            raise ValueError(
                u"control characters must only be a single character")

        # set the attribute dynamically.
        if not hasattr(self, cc_type):
            raise AttributeError(
                u"{} doesn't have an attribute with the name '{}'".format(
                    self, cc_type)
            )

        other = copy(self)
        setattr(other, cc_type, char)

        # return clone
        return other

    def __str__(self):
        return u''.join([self.component_separator,
                        self.data_separator,
                        self.decimal_point,
                        self.escape_character,
                        self.reserved_character,
                        self.segment_terminator])

    def __repr__(self):
        return u"'{}'".format(self.__str__())

    def __eq__(self, other):
        return (self.component_separator == other.component_separator) and \
            (self.data_separator == other.data_separator) and \
            (self.decimal_point == other.decimal_point) and \
            (self.escape_character == other.escape_character) and \
            (self.reserved_character == other.reserved_character) and \
            (self.segment_terminator == other.segment_terminator)
