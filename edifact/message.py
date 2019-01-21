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
from __future__ import with_statement
from __future__ import absolute_import
from edifact.parser import Parser
from edifact.serializer import Serializer
import codecs
from io import open


class Message(object):
    u"""Represent an EDI message for both reading and writing."""

    def __init__(self):

        # The segments that make up this message
        self.segments = []

        # Flag whether the UNA header is present
        self.has_una_segment = False

    @classmethod
    def from_file(cls, file, encoding=u'iso8859-1'):
        u"""Create a Message instance from a file.

        Raises FileNotFoundError if filename is not found.
        :param encoding: an
        :param file: The full path to a file that contains an EDI message
        :rtype: Message
        """

        # codecs.lookup raises an LookupError if given codec was not found:
        codecs.lookup(encoding)

        with open(file, encoding=encoding) as f:
            message = f.read()
        return cls.from_str(message)

    @classmethod
    def from_str(cls, string):
        u"""Create a Message instance from a string.
        :param string: The EDI message content
        :rtype: Message
        """
        segments = Parser().parse(string)

        return cls.from_segments(segments)

    @classmethod
    def from_segments(cls, segments):
        u"""Create a new Message instance from a iterable list of segments.

        :param segments: The segments of the message
        :type segments: list/iterable of Segment
        :rtype Message
        """

        # create a new instance of Message and return it
        # with the added segments
        return cls().add_segments(segments)

    def get_segments(self, name):
        u"""Get all the segments that match the requested name.
        :param name: The name of the segment to return
        :rtype: list of Segment
        """
        for segment in self.segments:
            if segment.tag == name:
                yield segment

    def get_segment(self, name):
        u"""Get the first segment that matches the requested name.

         :return: The requested segment, or None if not found
        :param name: The name of the segment to return
        """
        for segment in self.get_segments(name):
            return segment

        return None

    def add_segments(self, segments):
        u"""Add multiple segments to the message.

        :param segments: The segments to add
        :type segments: list or iterable of Segments
        """
        for segment in segments:
            self.add_segment(segment)

        return self

    def add_segment(self, segment):
        u"""Append a segment to the message.

        :param segment: The segment to add
        """
        if segment.tag == u"UNA":
            self.has_una_segment = True
        self.segments.append(segment)
        return self

    def serialize(self):
        u"""Serialize all the segments added to this object."""
        return Serializer().serialize(self.segments, self.has_una_segment)

    def __str__(self):
        u"""Allow the object to be serialized by casting to a string."""
        return self.serialize()
