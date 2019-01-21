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
from __future__ import with_statement
from __future__ import absolute_import
from edifact.segments import Segment
import unittest


class SegmentTest(unittest.TestCase):

    def setUp(self):
        self.elements = [
            u"field1",
            [u"field2", u"extra"],
            u"stuff",
        ]

    def test_get_segment_code(self):
        segment = Segment(u"OMD")
        self.assertEqual(u"OMD", segment.tag)

    def test_all_elements(self):
        segment = Segment(u"OMD", *self.elements)
        self.assertEqual(self.elements, segment.elements)

    def test_get_single_element(self):
        segment = Segment(u"OMD", *self.elements)
        self.assertEqual(u"field1", segment.elements[0])

    def test_get_list_element(self):
        segment = Segment(u"OMD", *self.elements)
        self.assertEqual([u"field2", u"extra"], segment.elements[1])

    def test_get_non_existing_element(self):
        segment = Segment(u"OMD", *self.elements)
        with self.assertRaises(IndexError):
            segment.elements[7]


if __name__ == u'__main__':
    unittest.main()
