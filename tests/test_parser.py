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
from edifact.parser import Parser
from edifact.segments import Segment
import unittest


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.default_una_segment = Segment(u'UNA', u":+,? '")

    def test_setup_special_characters1(self):
        message = self.parser.get_control_characters(u"TEST")
        self.assertEqual(u":+,? '", str(message))

    def test_setup_special_characters2(self):
        message = self.parser.get_control_characters(u"UNA123456")
        self.assertEqual(u"123456", str(message))

    def test_setup_special_characters3(self):

        message = self.parser.get_control_characters(u"UNA123456TEST")
        self.assertEqual(u"123456", str(message))

    def test_setup_special_characters4(self):

        message = self.parser.get_control_characters(u"UNA123456\nTEST")
        self.assertEqual(u"123456", str(message))

    def test_setup_special_characters5(self):

        message = self.parser.get_control_characters(u"UNA123456\r\nTEST")
        self.assertEqual(u"123456", str(message))

    def _assert_segments(self, message, segments):
        """This function asserts that the given message, when parsed with
        Parser.parse(), produces exactly the list output given by segments.
        :param message: The message to parse. The UNA string is added.
        :param segments: The expected segments list
        """

        input_str = u"UNA:+,? '\n" + message + u"'\n"
        result = list(self.parser.parse(input_str))
        self.assertEquals([self.default_una_segment] + segments, result)

    def test_compare_equal_segments(self):
        """Just make sure that comparing Segment objects works"""
        a = [Segment(u"RFF", [u"PD", u"50515"])]
        b = [Segment(u"RFF", [u"PD", u"50515"])]
        assert a is not b, \
            u"Two separatedly created Segment objects may not be a singleton."
        self.assertEqual(a, b)

    def test_una_parser1(self):
        # UNA headers are a special parsing task and must be processed
        # correctly.
        tokens = self.parser.parse(u"UNA:+,? 'TEST'")
        self.assertEqual(tokens.next(), Segment(u'UNA', u":+,? '"))
        self.assertEqual(tokens.next(), Segment(u'TEST'))

    def test_una_parser2(self):
        # UNA headers are a special parsing task and must be processed
        # correctly.
        tokens = self.parser.parse(u"UNA123456TEST6")
        self.assertEqual(tokens.next(), Segment(u'UNA', u"123456"))
        self.assertEqual(tokens.next(), Segment(u'TEST'))

    def test_una_parser3(self):
        # UNA headers are a special parsing task and must be processed
        # correctly.
        tokens = self.parser.parse(u"UNA12345'TEST'")
        self.assertEqual(tokens.next(), Segment(u'UNA', u"12345'"))
        self.assertEqual(tokens.next(), Segment(u'TEST'))

    def test_basic1(self):

        self._assert_segments(u"RFF+PD:50515", [
            Segment(u"RFF", [u"PD", u"50515"]),
        ])

    def test_basic2(self):

        self._assert_segments(u"RFF+PD+50515", [
            Segment(u"RFF", u"PD", u"50515"),
        ])

    def test_escape_character(self):

        self._assert_segments(u"ERC+10:The message does not make sense??", [
            Segment(u"ERC", [u"10", u"The message does not make sense?"]),
        ])

    def test_escape_component_separator(self):

        self._assert_segments(u"ERC+10:Name?: Craig", [
            Segment(u"ERC", [u"10", u"Name: Craig"]),
        ])

    def test_escape_data_separator(self):

        self._assert_segments(u"DTM+735:?+0000:406", [
            Segment(u"DTM", [u"735", u"+0000", u"406"]),
        ])

    def test_escape_decimal_point(self):

        self._assert_segments(u"QTY+136:12,235", [
            Segment(u"QTY", [u"136", u"12,235"]),
        ])

    def test_escape_segment_terminator(self):

        self._assert_segments(u"ERC+10:Craig?'s", [
            Segment(u"ERC", [u"10", u"Craig's"]),
        ])

    def test_escape_sequence(self):

        self._assert_segments(u"ERC+10:?:?+???' - ?:?+???' - ?:?+???'", [
            Segment(u"ERC", [u"10", u":+?' - :+?' - :+?'"]),
        ])


if __name__ == u'__main__':
    unittest.main()
