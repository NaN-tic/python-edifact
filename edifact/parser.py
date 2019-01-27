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
from edifact.tokenizer import Tokenizer
from edifact.token import Token
from edifact.segments import SegmentFactory
from edifact.control import Characters
from builtins import range


class Parser(object):
    u"""Parse EDI messages into a list of segments."""

    def __init__(self, factory=None):
        if factory is None:
            factory = SegmentFactory()

        self.factory = factory
        self.characters = Characters()

    def parse(self, message, characters=None):
        u"""Parse the message into a list of segments.

        :param characters: the control characters to use, if there is no
                UNA segment present
        :param message: The EDI message
        :rtype:
        """

        # FIXME: DRY: use get_control_characters here?
        tokens = []
        # If there is a UNA token, take the following 6 characters
        # unconditionally, save them as token and use it as control characters
        # for further parsing
        if message[0:3] == u'UNA':
            control_chars = message[3:9]
            tokens.append(Token(Token.Type.CONTENT, u'UNA'))
            tokens.append(Token(Token.Type.CTRL_CHARS, control_chars))

            # remove the UNA segment from the string
            message = message[9:].lstrip(u"\r\n")
            self.characters = Characters.from_str(u'UNA' + control_chars)

        else:
            # if no UNA header present, use default control characters
            if characters is not None:
                self.characters = characters

        tokenizer = Tokenizer()
        tokens += tokenizer.get_tokens(message, self.characters)
        segments = self.convert_tokens_to_segments(tokens, self.characters)
        return segments

    @staticmethod
    def get_control_characters(message, characters=None):
        u"""Read the UNA segment from the passed string.

        :param message: a valid EDI message string, or UNA segment string,
                        to extract the control characters from
        :param characters: the control characters to use, if none found in
                           the message
        :rtype: str or None
        :return: the control characters
        """

        if not characters:
            characters = Characters()

        # First, try to read the UNA segment ("Service String Advice",
        # conditional). This segment and the UNB segment (Interchange Header)
        # must always be written in ASCII, even if after the BGM the files
        # continues with cyrillic or UTF-16.

        # If it does not exist, return a default.
        if not message[:3] == u"UNA":
            return characters

        # Get the character definitions
        chars = message[3:9]
        characters.is_extracted_from_message = True

        characters.component_separator = chars[0]
        characters.data_separator = chars[1]
        characters.decimal_point = chars[2]
        characters.escape_character = chars[3]
        characters.reserved_character = chars[4]
        characters.segment_terminator = chars[5]

        return characters

    def convert_tokens_to_segments(self, tokens, characters, with_una=False):
        u"""Convert the tokenized message into an array of segments.
        :param with_una: whether the UNA segment should be included
        :param tokens: The tokens that make up the message
        :param characters: the control characters to use
        :type tokens: list of Token
        :rtype list of Segment
        """

        segments = []
        current_segment = []
        data_element = None
        in_segment = False
        empty_component_counter = 0

        previous_token = None
        for token in tokens:
            # If we're in the mid of a segment, check if we've reached the end
            if in_segment:

                # a UNA control character string is a special case.
                # It has no data terminator, as the last character DEFINES the
                # data terminator.
                # So we must handle the string as content, AND terminator
                # at the same time.
                if token.type == Token.Type.CTRL_CHARS:
                    in_segment = False
                    current_segment.append(data_element[0])
                    current_segment.append(token.value)
                    data_element = []
                    previous_token = token
                    continue

                if token.type == Token.Type.TERMINATOR:
                    in_segment = False
                    if len(data_element) == 0:  # empty element
                        data_element = u''
                    elif len(data_element) == 1:
                        # use a str instead of a list
                        data_element = data_element[0]
                    else:
                        if previous_token.type == Token.Type.COMPONENT_SEPARATOR:
                            data_element.append(u'')
                    current_segment.append(data_element)
                    data_element = []
                    previous_token = token
                    empty_component_counter = 0
                    continue

            # If we're not in a segment, then start a new empty one now
            # and add it to the list. Also create a new empty data element,
            # because if the next token is a DATA_SEPARATOR, at least we have
            # an empty string to save into the segment then.
            else:
                current_segment = []
                segments.append(current_segment)
                data_element = []
                in_segment = True

            # Whenever we reach a data separator (+), we add the currently
            # collected data element to the current segment and reset the
            # data_element to an empty list []
            if token.type == Token.Type.DATA_SEPARATOR:
                if len(data_element) == 0:  # empty element
                    data_element = u''
                elif len(data_element) == 1:
                    data_element = data_element[0]

                current_segment.append(data_element)

                data_element = []
                empty_component_counter = 0
                previous_token = token
                continue

            # Whenever we reach a component data separator (:), we know that
            # the whole data element is a composite, so increment the counter
            # this is especially needed when more than one component data
            # separators are in a row "23:::56"
            if token.type == Token.Type.COMPONENT_SEPARATOR:
                empty_component_counter += 1
                previous_token = token
                continue

            # here we can be sure that the token value is normal "content"
            # first backfill empty strings for skipped component data (:::)
            for i in range(0, empty_component_counter):
                data_element.append(u'')

            data_element.append(token.value)
            empty_component_counter = 0
            previous_token = token
            continue
        for segment in segments:
            name = segment.pop(0)
            yield self.factory.create_segment(characters, name, *segment)
