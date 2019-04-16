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
from edifact.control.characters import Characters
import re
from builtins import map

try:
    str = unicode
except NameError:
    pass


class Serializer(object):
    u"""Serialize a bunch of segments into an EDI message string."""

    def __init__(self, characters=None):
        super(Serializer, self).__init__()
        if characters is None:
            characters = Characters()

        self.characters = characters

    def serialize(self, segments, with_una=False):
        u"""Serialize all the passed segments.

        :param segments: a list of segments to serialize
        :param with_una: flag if a UNA header should be written
        """

        message = u''

        if with_una:
            # create an EDIFACT header
            message = u"UNA"
            message += self.characters.component_separator
            message += self.characters.data_separator
            message += self.characters.decimal_point
            message += self.characters.escape_character
            message += self.characters.reserved_character
            message += self.characters.segment_terminator

        # iter through all segments
        for segment in segments:
            # skip the UNA segment as we already have written it if requested
            if segment.tag == u'UNA':
                continue
            message += segment.tag
            for element in segment.elements:
                message += self.characters.data_separator
                if type(element) == list:
                    for nr, subelement in enumerate(element):
                        element[nr] = self.escape(subelement)
                    message += u''.join([self.characters.component_separator if
                                        x == u'' else x for x in element])
                else:
                    message += self.escape(element)

            message += self.characters.segment_terminator

        return message

    def escape(self, string):
        u"""Escapes control characters.

        :param string the string to be escaped
        """
        assert(type(string) == str)

        characters = [
            self.characters.component_separator,
            self.characters.data_separator,
            self.characters.segment_terminator,
        ]
        replace_map = {}
        for char in characters:
            replace_map[char] = self.characters.escape_character + char

        # Thanks to "Bor González Usach" for this wonderful piece of code:
        # https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
        substrs = sorted(replace_map, key=len, reverse=True)
        regexp = re.compile(u'|'.join(map(re.escape, substrs)))

        return regexp.sub(lambda match: replace_map[match.group(0)], string)
