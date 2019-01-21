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
import unittest
from edifact.token import Token


class TokenTest(unittest.TestCase):

    def test_type(self):
        token = Token(Token.Type.CONTENT, u"ok")
        self.assertEqual(Token.Type.CONTENT, token.type)

    def test_value(self):
        token = Token(Token.Type.CONTENT, u"ok")
        self.assertEqual(u"ok", token.value)


if __name__ == u'__main__':
    unittest.main()
