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
from edifact.token import Token
from edifact.tokenizer import Tokenizer
import unittest

from edifact.control.characters import Characters


class TokenizerTest(unittest.TestCase):

    def setUp(self):
        self._tokenizer = Tokenizer()

    def _assert_tokens(self, message, expected=None):
        if expected is None:
            expected = []
        tokens = self._tokenizer.get_tokens(
            u"{}'".format(message), Characters())
        expected.append(Token(Token.Type.TERMINATOR, u"'"))
        self.assertEqual(expected, tokens)

    def test_basic(self):
        self._assert_tokens(u"RFF+PD:50515", [
            Token(Token.Type.CONTENT, u"RFF"),
            Token(Token.Type.DATA_SEPARATOR, u"+"),
            Token(Token.Type.CONTENT, u"PD"),
            Token(Token.Type.COMPONENT_SEPARATOR, u":"),
            Token(Token.Type.CONTENT, u"50515"),
        ])

    def test_escape(self):
        self._assert_tokens(u"RFF+PD?:5", [
            Token(Token.Type.CONTENT, u"RFF"),
            Token(Token.Type.DATA_SEPARATOR, u"+"),
            Token(Token.Type.CONTENT, u"PD:5"),
        ])

    def test_double_escape(self):
        self._assert_tokens(u"RFF+PD??:5", [
            Token(Token.Type.CONTENT, u"RFF"),
            Token(Token.Type.DATA_SEPARATOR, u"+"),
            Token(Token.Type.CONTENT, u"PD?"),
            Token(Token.Type.COMPONENT_SEPARATOR, u":"),
            Token(Token.Type.CONTENT, u"5"),
        ])

    def test_triple_escape(self):
        self._assert_tokens(u"RFF+PD???:5", [
            Token(Token.Type.CONTENT, u"RFF"),
            Token(Token.Type.DATA_SEPARATOR, u"+"),
            Token(Token.Type.CONTENT, u"PD?:5"),
        ])

    def test_quadruple_escape(self):
        self._assert_tokens(u"RFF+PD????:5", [
            Token(Token.Type.CONTENT, u"RFF"),
            Token(Token.Type.DATA_SEPARATOR, u"+"),
            Token(Token.Type.CONTENT, u"PD??"),
            Token(Token.Type.COMPONENT_SEPARATOR, u":"),
            Token(Token.Type.CONTENT, u"5"),
        ])

    def test_ignore_whitespace(self):
        self._assert_tokens(u"RFF:5'\nDEF:6", [
            Token(Token.Type.CONTENT, u"RFF"),
            Token(Token.Type.COMPONENT_SEPARATOR, u":"),
            Token(Token.Type.CONTENT, u"5"),
            Token(Token.Type.TERMINATOR, u"'"),
            Token(Token.Type.CONTENT, u"DEF"),
            Token(Token.Type.COMPONENT_SEPARATOR, u":"),
            Token(Token.Type.CONTENT, u"6"),
        ])

    def test_no_terminator(self):
        with self.assertRaises(RuntimeError) as cm:
            self._tokenizer.get_tokens(u"TEST", Characters())
        self.assertEqual(
            str(cm.exception), "Unexpected end of EDI message")


if __name__ == u'__main__':
    unittest.main()
