# encoding: utf8
##############################################################################
#
#    Copyright (C) 2011-2018 NaN Projectes de Programari Lliure, S.L.
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
from edifact.segments import Segment
from edifact.serializer import Serializer
import unittest


class SerializerTest(unittest.TestCase):

    def setUp(self):
        self.serializer = Serializer()

    def assert_segments(self, expected, segments):
        expected = u"UNA:+,? '\n" + expected + u"'"+'\n'
        message = self.serializer.serialize(segments, with_una=True)
        self.assertEqual(expected, message)

    def test_basic1(self):
        self.assert_segments(u"RFF+PD:50515", [
            Segment(u"RFF", [u"PD", u"",  u"50515"]),
        ])

    def test_basic2(self):
        self.assert_segments(u"RFF+PD+50515", [
            Segment(u"RFF", u"PD", u"50515"),
        ])

    def test_escape_character(self):
        self.assert_segments(u"ERC+10:The message does not make sense?", [
            Segment(u"ERC", [u"10", u"", u"The message does not make sense?"]),
        ])

    def test_escape_component_separator(self):
        self.assert_segments(u"ERC+10:Name?: Craig", [
            Segment(u"ERC", [u"10", u"", u"Name: Craig"]),
        ])

    def test_escape_data_separator(self):
        self.assert_segments(u"DTM+735:?+0000:406", [
            Segment(u"DTM", [u"735", u"", u"+0000", u"", u"406"]),
        ])

    def test_escape_decimal_point(self):
        self.assert_segments(u"QTY+136:12,235", [
            Segment(u"QTY", [u"136", u"", u"12,235"]),
        ])

    def test_escape_segment_terminator(self):
        self.assert_segments(u"ERC+10:Craig?'s", [
            Segment(u"ERC", [u"10", u"", u"Craig's"]),
        ])

    def test_escape_sequence(self):
        self.assert_segments(u"ERC+10:?:?+??' - ?:?+??' - ?:?+??'", [
            Segment(u"ERC", [u"10", u"", u":+?' - :+?' - :+?'"]),
        ])


if __name__ == u'__main__':
    unittest.main()
