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
import unittest

from edifact.control.characters import Characters


class TestControlCharacters(unittest.TestCase):

    def setUp(self):
        self.cc = Characters()

    def test_wrong_attribute(self):
        self.assertRaises(AttributeError, self.cc.with_control_character,
                          u'wrongtype', u'+')

    def test_wrong_character_size(self):
        self.assertRaises(ValueError, self.cc.with_control_character,
                          u'decimal_point', u',.')

    def test_correct_parameters(self):

        self.assertEqual(self.cc.with_control_character(
            u'component_separator', u'/').component_separator, u'/')

        self.assertEqual(self.cc.with_control_character(
            u'data_separator', u'/').data_separator, u'/')

        self.assertEqual(self.cc.with_control_character(
            u'decimal_point', u'/').decimal_point, u'/')

        self.assertEqual(self.cc.with_control_character(
            u'escape_character', u'/').escape_character, u'/')

        self.assertEqual(self.cc.with_control_character(
            u'reserved_character', u'/').reserved_character, u'/')

        self.assertEqual(self.cc.with_control_character(
            u'segment_terminator', u'/').segment_terminator, u'/')
